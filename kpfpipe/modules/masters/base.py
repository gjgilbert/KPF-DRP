from kpfpipe.data_models.level0 import KPF0
from kpfpipe.modules.image_assembly import ImageAssembly
from kpfpipe.utils import get_datecode, fetch_filepath
from kpfpipe.constants import NROW, NCOL

class BaseMastersModule:
    def __init__(self, obs_ids):
        self.obs_ids = obs_ids


    @staticmethod
    def load_frame(obs_id):
        datecode = get_datecode(obs_id)
        filepath = fetch_filepath(obs_id)

        l0_obj = KPF0.from_fits(filepath)

        return l0_obj


    @staticmethod
    def assemble_frame(l0_obj):
        return ImageAssembly(l0_obj).perform()


    def compute_streaming_mean_and_variance(self, sigma_clip=3.0):
        """
        Computes mean and variance using Huber estimator
        Optimized to reduce RAM usage at the expense of compute speed

        # TODO: switch back to classic Welford for first 5-10 frames
        """
        mean = np.zeros((NROW,NCOL), dtype=float)
        M2 = np.zeros_like(mean, dtype=float)
        weight = np.zeros_like(mean, dtype=float)

        for i, obs_id in enumerate(self.obs_ids):
            try:
                l0_obj = self.load_frame(obs_id)
                frame = self.assemble_frame(l0_obj)
            except Exception as e:
                logger.warning(f"Skipping {obs_id} in initial pass: {e}")
                continue

            # TODO: scale by exposure time
            var = np.where(weight > 0, M2 / weight, 0.0)
            std = np.sqrt(var)
            
            s = np.where(std > 0, std, 1.0)
            r = (frame - mean) / s
            
            w = np.minimum(1.0, sigma_clip / np.abs(r))
            w = np.where(np.isfinite(w), w, 1.0)

            weight += w
            delta = frame - mean
            mean += w * delta / weight
            M2 += w * delta * (frame - mean)

        var = np.where(weight > 0, M2 / weight, 0.0)

        return mean, var
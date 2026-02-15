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
        Computes mean and variance using Welford's algorithm
        Optimized to reduce RAM usage at the expense of compute speed
        """
        # 1st pass: unclipped mean and variance
        mean = np.zeros((NROW,NCOL), dtype=float)
        M2 = np.zeros_like(mean, dtype=float)
        
        n = 0

        for i, obs_id in enumerate(self.obs_ids):
            try:
                l0_obj = self.load_frame(obs_id)
                frame = self.assemble_frame(l0_obj)
            except Exception as e:
                logger.warning(f"Skipping {obs_id} in initial pass: {e}")
                continue

            # TODO: scale by exposure time
            n += 1
            delta = frame - mean
            mean += delta / n
            M2 += delta * (frame - mean)

            xmin = np.minimum(frame, xmin)
            xmax = np.maximum(frame, xmax)

        var = M2 / (n - 1)

        if not sigma_clip:
            return mean, var
        
        # 2nd pass: clipped mean and variance
        clipped_sum = np.zeros_like(mean, dtype=float)
        clipped_sum2 = np.zeros_like(mean, dtype=float)
        count = np.zeros_like(mean, dtype=int)

        for i, obs_id in enumerate(self.obs_ids):
            try:
                l0_obj = self.load_frame(obs_id)
                frame = self.assemble_frame(l0_obj)
            except Exception as e:
                logger.warning(f"Skipping {obs_id} in sigma-clipping pass: {e}")
                continue

            lower = mean - sigma_clip * np.sqrt(var)
            upper = mean + sigma_clip * np.sqrt(var)
            mask = (frame >= lower) & (frame <= upper)

            clipped_sum += frame * mask
            clipped_sum2 += frame ** 2 * mask
            count += mask.astype(int)
    
        if np.any(count == 0):
            raise ValueError(f"Found {np.sum(count==0)} pixels with zero valid frames")

        count = np.where(count == 0, 1, count)
        clipped_mean = clipped_sum / count
        clipped_var = clipped_sum2 / count - clipped_mean ** 2

        return clipped_mean, clipped_var
from kpfpipe.data_models.level0 import KPF0
from kpfpipe.data_models.level1 import KPF1
from kpfpipe.data_models.ffi import KPF_FFI

from kpfpipe.modules.exposure_time import ExposureTime
from kpfpipe.modules.image_assembly import ImageAssembly
from kpfpipe.modules.image_processing import ImageProcessing
from kpfpipe.modules.spectral_extraction import SpectralExtraction
from kpfpipe.modules.wavelength_calibration import WavelengthCalibration
from kpfpipe.modules.barycentric_correction import BarycentricCorrection

from kpfpipe.utils import get_datecode, fetch_filepath, fetch_master_path


def main():
    print("\n\n=== entering kpf_drp_science pipeline ===\n\n")
    
    # Load target observation and corresponding masters
    obs_id = 'KP.YYYYMMDD.NNNNN.NN'
    datecode = get_datecode(obs_id)
    filpath = fetch_filepath(obs_id)
    target_l0 = KPF0.from_fits(obs_id)

    flat = KPF_FFI.from_fits(fetch_master_path(datecode, 'flat'))
    dark = KPF_FFI.from_fits(fetch_master_path(datecode, 'dark'))
    bias = KPF_FFI.from_fits(fetch_master_path(datecode, 'bias'))
    wls = KPF_FFI.from_fits(fetch_master_path(datecode, 'thar-wls'))

    # Perform L0 --> L1 data processing algorithms
    exposure_time = ExposureTime(target_l0)
    target_l0 = exposure_time.perform()

    image_assembly = ImageAssembly(target_l0)
    target_ffi = image_assembly.perform()

    image_processing = ImageProcessing(target_ffi)
    target_ffi = image_processing.perform(flat, dark, bias)

    spectral_extraction = SpectralExtraction(target_ffi)
    target_l1 = spectral_extraction.perform()

    wavelength_calibration = WavelengthCalibration(target_l1)
    target_l1 = wavelength_calibration.perform()

    barycentric_correction = BarycentricCorrection(target_l1)
    target_l1 = barycentric_correction.perform()

    # Save L1 file to disk
    target_l1.to_fits()

    print("\n\n=== exiting kpf_drp_science pipeline ===\n\n")


if __name__ == '__main__':
    main()
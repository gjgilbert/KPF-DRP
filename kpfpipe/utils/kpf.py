def get_datecode(input_str):
    """
    Extract the datecode from an obs_id or filename

    Args:
        input_str, e.g. 'KP.20230708.04519.63' or 'KP.20230708.04519.63_2D.fits'

    Returns:
        datecode, e.g. '20230708'
    """
    if is_obs_id(input_str):
        obs_id = input_str
    else:
        obs_id = get_obs_id(filename)
    
    datecode = obs_id.split('.')[1]

    return datecode


def get_obs_id(filename):
    """
    Extracts an obs_id from a filename
    
    Args:
        filename, e.g. '/data/L1/20240113/KP.20240113.23249.10_L1.fits').

    Returns:
        obs_id, e.g. 'KP.20240113.23249.10'
    """
    # TODO: modify to properly handle masters files
    obs_id = file.split('/')[-1]
    for substring in ['.fits', '_2D', '_L1', '_L2']:
        obs_id = obs_id.replace(substring, '')
    return obs_id


def is_obs_id(obs_id):
    """
    Returns True if the input is a properly formatted ObsID, e.g. 'KP.20240113.23249.10'
    """
    pattern = r'^KP\.\d{8}\.\d{5}\.\d{2}$'
    is_obs_id_bool = bool(re.match(pattern, obs_id))
    return is_obs_id_bool


def fetch_filepath(obs_id, level, fullpath=False):
    pass


def fetch_master_filepath(obs_id, master, fullpath=False):
    pass


def get_orderlet_ext_from_fiber_name(chip, fiber):
    flux_dict = {'SKY': f'{chip}_SKY_FLUX',
                'SCI1': f'{chip}_SCI_FLUX1',
                'SCI2': f'{chip}_SCI_FLUX2',
                'SCI3': f'{chip}_SCI_FLUX3',
                'CAL': f'{chip}_CAL_FLUX'
                }

    var_dict = {'SKY': f'{chip}_SKY_VAR',
                'SCI1': f'{chip}_SCI_VAR1',
                'SCI2': f'{chip}_SCI_VAR2',
                'SCI3': f'{chip}_SCI_VAR3',
                'CAL': f'{chip}_CAL_VAR'
            }

    wave_dict = {'SKY': f'{chip}_SKY_WAVE',
                 'SCI1': f'{chip}_SCI_WAVE1',
                 'SCI2': f'{chip}_SCI_WAVE2',
                 'SCI3': f'{chip}_SCI_WAVE3',
                 'CAL': f'{chip}_CAL_WAVE'
            }
    
    return flux_dict[fiber], var_dict[fiber], wave_dict[fiber]

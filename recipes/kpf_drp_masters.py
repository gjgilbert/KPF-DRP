from kpfpipe.modules.masters.bias import Bias
from kpfpipe.modules.masters.dark import Dark
from kpfpipe.modules.masters.flat import Flat
from kpfpipe.modules.masters.wls import WLS

from kpfpipe.utils import query_db_for_masters_stack

def main():
    print("\n\n=== entering kpf_drp_masters pipeline ===\n\n")
    
    datecode = 'YYYYMMDD'

    bias = Bias(query_db_for_masters_stack(datecode, 'bias'))
    bias.make_master()

    dark = Dark(query_db_for_masters_stack(datecode), 'dark')
    dark.make_master()

    flat = Flat(query_db_for_masters_stack(datecode), 'flat')
    flat.make_master()

    wls = WLS(query_db_for_masters_stack(datecode), 'thar-wls')
    wls.make_master()

    print("\n\n=== exiting kpf_drp_masters pipeline ===\n\n")


if __name__ == '__main__':
    main()
import os.path as op
import argparse
from bv2mne.config.config import setup_db_coords
# setup_db_coords(op.join('D:\\', 'Databases', 'toy_db'), 'meg_causal', overwrite=True)
from bv2mne.directories import create_sbj_db_mne

def create_main(data, project, subjects, ses, event, json):

    if not json:
        json = setup_db_coords(data, project , overwrite=True)

    from bv2mne.source import create_source_models
    from bv2mne.forward import create_forward_models

    #subjects = ['subject_16']

    for sbj in subjects:

        create_sbj_db_mne (json, sbj)
        # Pipeline for the estimation of surfaces/volumes sources and labels
        # ------------------------------------------------------------------------------------------------------------------
        surf_src, surf_labels, vol_src, vol_labels = create_source_models(json, sbj, save=True)
        # ------------------------------------------------------------------------------------------------------------------

        # Pipeline to estimate surfaces/volumes forward models
        # ------------------------------------------------------------------------------------------------------------------
        fwds = create_forward_models(json, sbj, ses, event)
        # ------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # Command line parser
    parser = argparse.ArgumentParser(
        description="BV 2 MNE transformation ")

    parser.add_argument("-data", dest="data", type=str, required=True,
                        help="Directory containing data ")

    parser.add_argument("-project", dest="project", type=str,
                        default = "meg_causal", help="Project name",
                        required=False)

    parser.add_argument("-subjects", dest="subjects", type=str, nargs='+',
                        help="Subjects ID", required=True)

    parser.add_argument("-event", dest="event", type=str,
                        help="Event Name", required=True)

    parser.add_argument("-ses", dest="ses", type=str,
                        help="ses number", required=True)

    parser.add_argument("-json", dest="json", type=str,
                        help="If a json is alreasdy defined", required=False)

    args = parser.parse_args()

    # main_workflow
    print("Initialising the pipeline...")
    wf = create_main(
        data=args.data,
        project=args.project,
        subjects=args.subjects,
        ses=args.ses,
        event=args.event,
        json=args.json
    )

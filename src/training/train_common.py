import os

import shared_variables


def create_checkpoints_path(log_name, models_folder, fold, model_type):
    folder_path = shared_variables.outputs_folder + models_folder + '/' + str(fold) + '/models/' + model_type + '/' + \
                  log_name + '/'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    checkpoint_name = folder_path + 'model_{epoch:03d}-{val_loss:.3f}.h5'
    return checkpoint_name

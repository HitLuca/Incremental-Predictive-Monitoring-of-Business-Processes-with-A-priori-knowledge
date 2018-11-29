import glob
import os


def main():
    experiments_folder = 'output_files/final_experiments_'

    for i in range(1, 5):
        current_experiments_folder = experiments_folder + str(i) + '/models/'
        for model_type in os.listdir(current_experiments_folder):
            model_folder = current_experiments_folder + model_type + '/'
            print(model_folder)

            for log_name in os.listdir(model_folder):
                log_folder = model_folder + log_name + '/'
                print(log_folder)

                checkpoints = glob.glob(log_folder + '*.h5')

                if len(checkpoints) > 1:
                    checkpoints.sort(key=os.path.getctime)

                    for checkpoint in checkpoints[:-1]:
                        os.remove(checkpoint)


if __name__ == '__main__':
    main()
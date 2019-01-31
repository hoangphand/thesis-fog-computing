import random
from processor import Processor

class ProcessorDAG(object):
    NUMBER_OF_FOGS_LOWER_BOUND = 15
    NUMBER_OF_FOGS_UPPER_BOUND = 15
    NUMBER_OF_CLOUDS_LOWER_BOUND = 25
    NUMBER_OF_CLOUDS_UPPER_BOUND = 25

    """docstring for ProcessorDAG"""
    def __init__(self):
        super(ProcessorDAG, self).__init__()
        self.fogs = []
        self.clouds = []
        
    def random_init(self):
        no_of_fogs = int(random.uniform(self.__class__.NUMBER_OF_FOGS_LOWER_BOUND, 
            self.__class__.NUMBER_OF_FOGS_UPPER_BOUND))
        no_of_clouds = int(random.uniform(self.__class__.NUMBER_OF_CLOUDS_LOWER_BOUND, 
            self.__class__.NUMBER_OF_CLOUDS_UPPER_BOUND))

        for i in range(0, no_of_fogs):
            new_fog = Processor(True)
            new_fog.generate_random_values()
            self.fogs.append(new_fog)

        for i in range(0, no_of_clouds):
            new_cloud = Processor(False)
            new_cloud.generate_random_values()
            self.clouds.append(new_cloud)

    def export_dag(self, output_file_path):
        with open(output_file_path, "w") as output:
            output.write(str(len(self.fogs)))
            output.write("\n")
            output.write(str(len(self.clouds)))
            output.write("\n")
            max_id_width = len("id")
            max_is_fog_width = len("is fog?")
            max_proc_rate_width = len("proc. rate")
            max_ram_width = len("ram   ")
            max_storage_width = len("storage")
            max_up_band_width = len("up band.")
            max_down_band_width = len("down band.")

            output.write("{1:<{0}s}\t\t{3:<{2}s}\t\t{5:<{4}s}\t\t{7:<{6}s}\t\t{9:<{8}s}\t\t{11:<{10}s}\t\t{13:<{12}s}"
                .format(
                    max_id_width, "id",
                    max_is_fog_width, "is fog?",
                    max_proc_rate_width, "proc. rate",
                    max_ram_width, "ram   ",
                    max_storage_width, "storage",
                    max_up_band_width, "up band.",
                    max_down_band_width, "down band."))

            output.write("\n")

            max_width_pred = max_id_width + max_is_fog_width + max_proc_rate_width + max_ram_width + max_storage_width + max_up_band_width + max_down_band_width + 12 * len("\t")

            for index in range(0, len(self.fogs)):
                output.write("{1:<{0}s}".format(max_id_width, str(index)))
                output.write("\t\t")
                output.write("{1:<{0}s}".format(max_is_fog_width, str(self.fogs[index].is_fog)))
                output.write("\t\t")
                output.write("{1:<{0}s}".format(max_proc_rate_width, str(self.fogs[index].processing_rate)))
                output.write("\t\t")
                output.write("{1:<{0}s}".format(max_ram_width, str(self.fogs[index].ram)))
                output.write("\t\t")
                output.write("{1:<{0}s}".format(max_storage_width, str(self.fogs[index].storage)))
                output.write("\t\t")
                output.write("{1:<{0}s}".format(max_up_band_width, str(self.fogs[index].wan_upload_bandwidth)))
                output.write("\t\t")
                output.write("{1:<{0}s}".format(max_down_band_width, str(self.fogs[index].wan_download_bandwidth)))
                output.write("\n")

            for index in range(0, len(self.clouds)):
                output.write("{1:<{0}s}".format(max_id_width, str(index)))
                output.write("\t\t")
                output.write("{1:<{0}s}".format(max_is_fog_width, str(self.clouds[index].is_fog)))
                output.write("\t\t")
                output.write("{1:<{0}s}".format(max_proc_rate_width, str(self.clouds[index].processing_rate)))
                output.write("\t\t")
                output.write("{1:<{0}s}".format(max_ram_width, str(self.clouds[index].ram)))
                output.write("\t\t")
                output.write("{1:<{0}s}".format(max_storage_width, str(self.clouds[index].storage)))
                output.write("\t\t")
                output.write("{1:<{0}s}".format(max_up_band_width, str(self.clouds[index].wan_upload_bandwidth)))
                output.write("\t\t")
                output.write("{1:<{0}s}".format(max_down_band_width, str(self.clouds[index].wan_download_bandwidth)))
                output.write("\n")

    def import_dag(self, input_file_path):
        with open(input_file_path, "r") as input:
            lines = input.readlines()
            no_of_fogs = int(''.join(char for char in lines[0] if char.isdigit()))
            no_of_clouds = int(''.join(char for char in lines[1] if char.isdigit()))

            current_line_index = 3

            self.fogs = []
            for i in range(0, no_of_fogs):
                details_of_row = [int(number) for number in lines[current_line_index].split()[2:7]]

                new_fog = Processor(True)
                new_fog.processing_rate = details_of_row[0]
                new_fog.ram = details_of_row[1]
                new_fog.storage = details_of_row[2]
                new_fog.wan_upload_bandwidth = details_of_row[3]
                new_fog.wan_download_bandwidth = details_of_row[4]

                self.fogs.append(new_fog)

                current_line_index += 1

            self.clouds = []
            for i in range(0, no_of_clouds):
                details_of_row = [int(number) for number in lines[current_line_index].split()[2:7]]

                new_cloud = Processor(False)
                new_cloud.processing_rate = details_of_row[0]
                new_cloud.ram = details_of_row[1]
                new_cloud.storage = details_of_row[2]
                new_cloud.wan_upload_bandwidth = details_of_row[3]
                new_cloud.wan_download_bandwidth = details_of_row[4]

                self.clouds.append(new_cloud)

                current_line_index += 1
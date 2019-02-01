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
        self.no_of_fogs = 0
        self.no_of_clouds = 0
        self.processors = []
        
    def random_init(self):
        self.no_of_fogs = int(random.uniform(self.__class__.NUMBER_OF_FOGS_LOWER_BOUND, 
            self.__class__.NUMBER_OF_FOGS_UPPER_BOUND))
        self.no_of_clouds = int(random.uniform(self.__class__.NUMBER_OF_CLOUDS_LOWER_BOUND, 
            self.__class__.NUMBER_OF_CLOUDS_UPPER_BOUND))

        index = 0
        for i in range(0, self.no_of_fogs):
            new_fog = Processor(id, True)
            new_fog.generate_random_values()
            self.processors.append(new_fog)
            index = i

        for i in range(index, self.no_of_fogs + self.no_of_clouds):
            new_cloud = Processor(id, False)
            new_cloud.generate_random_values()
            self.processors.append(new_cloud)

    def export_dag(self, output_file_path):
        with open(output_file_path, "w") as output:
            output.write(str(self.no_of_fogs))
            output.write("\n")
            output.write(str(self.no_of_clouds))
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

            for index in range(0, len(self.processors)):
                output.write("{1:<{0}s}".format(max_id_width, str(index)))
                output.write("\t\t")
                output.write("{1:<{0}s}".format(max_is_fog_width, str(self.processors[index].is_fog)))
                output.write("\t\t")
                output.write("{1:<{0}s}".format(max_proc_rate_width, str(self.processors[index].processing_rate)))
                output.write("\t\t")
                output.write("{1:<{0}s}".format(max_ram_width, str(self.processors[index].ram)))
                output.write("\t\t")
                output.write("{1:<{0}s}".format(max_storage_width, str(self.processors[index].storage)))
                output.write("\t\t")
                output.write("{1:<{0}s}".format(max_up_band_width, str(self.processors[index].wan_upload_bandwidth)))
                output.write("\t\t")
                output.write("{1:<{0}s}".format(max_down_band_width, str(self.processors[index].wan_download_bandwidth)))
                output.write("\n")

    def import_dag(self, input_file_path):
        with open(input_file_path, "r") as input:
            lines = input.readlines()
            self.no_of_fogs = int(''.join(char for char in lines[0] if char.isdigit()))
            self.no_of_clouds = int(''.join(char for char in lines[1] if char.isdigit()))

            current_line_index = 3

            self.processors = []
            for i in range(0, self.no_of_fogs + self.no_of_clouds):
                details_of_row = [int(number) for number in lines[current_line_index].split()[2:7]]

                is_fog = lines[current_line_index].split()[1] == "True"

                new_processor = Processor(i, is_fog)
                new_processor.processing_rate = details_of_row[0]
                new_processor.ram = details_of_row[1]
                new_processor.storage = details_of_row[2]
                new_processor.wan_upload_bandwidth = details_of_row[3]
                new_processor.wan_download_bandwidth = details_of_row[4]

                self.processors.append(new_processor)

                current_line_index += 1

    def get_most_powerful_processor(self):
        most_powerful_processor = self.processors[0]

        for i in range(1, len(self.processors)):
            if self.processors[i].processing_rate > most_powerful_processor.processing_rate:
                most_powerful_processor = self.processors[i]
        
        return most_powerful_processor

    @staticmethod
    def get_bandwidth_to_use(from_processor, to_processor):
        bandwidth_to_use = 0

        if from_processor.is_fog and to_processor.is_fog:
            bandwidth_to_use = Processor.BANDWIDTH_LAN
        else:
            bandwidth_to_use = min(from_processor.wan_upload_bandwidth, to_processor.wan_download_bandwidth)
        
        return bandwidth_to_use

    @staticmethod
    def get_communication_time(from_processor, to_processor, amount_of_data):
        communication_time = 0

        if from_processor.id == to_processor.id:
            communication_time = 0
        else:           
            bandwidth_to_use = ProcessorDAG.get_bandwidth_to_use(from_processor, to_processor)
            
            communication_time = amount_of_data / bandwidth_to_use
        
        return communication_time
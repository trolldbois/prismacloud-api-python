""" Prisma Cloud Compute API Logs Endpoints Class """

# Containers

class LogsPrismaCloudAPICWPPMixin:
    """ Prisma Cloud Compute API Logs Endpoints Class """

    # Undocumented endpoints.

    def agentless_logs_read(self, query_params=None):
        logs = self.execute_compute('GET', 'api/v1/logs/agentless/download', query_params=query_params)
        return logs

    def defender_logs_list_read(self, host_name, query_params=None):
        logs = self.execute_compute('GET', 'api/v1/logs/defender/download?hostname=%s' % host_name, query_params=query_params)
        return logs

    def console_logs_list_read(self, query_params=None):
        logs = self.execute_compute('GET', 'api/v1/logs/console', query_params=query_params)
        return logs

    def console_logs_list_download(self, query_params=None, stream=True):
        logs = self.execute_compute('GET', 'api/v1/logs/console/download', query_params=query_params, stream=stream)
        return logs

    # this doesn't exists 2026-01
    # def system_logs_list_read(self, query_params=None):
    #     logs = self.execute_compute('GET', 'api/v1/logs/system/download', query_params=query_params)
    #     return logs

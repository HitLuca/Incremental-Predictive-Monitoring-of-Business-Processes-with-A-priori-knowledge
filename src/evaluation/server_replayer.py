import subprocess

from py4j.java_gateway import JavaGateway, GatewayParameters

from shared_variables import get_int_from_unicode


class ServerReplayer:
    def __init__(self, port, python_port):
        self._port = port
        self._python_port = python_port

        self._gateway, self._traces_checker = None, None
        self._server_process = None

    def start_server(self):
        server_start_instructions = ['java', '-jar']
        server_args = ['../LTLCheckForTraces.jar', str(self._port), str(self._python_port)]

        self._server_process = subprocess.Popen(server_start_instructions + list(server_args))

        self._gateway = JavaGateway(gateway_parameters=GatewayParameters(port=self._port),
                                    python_proxy_port=self._python_port)
        self._traces_checker = self._gateway.entry_point

    def stop_server(self):
        self._server_process.terminate()
        self._server_process.wait()

    def verify_with_data(self, model_file, trace_id, activities, groups, times, prefix=0):
        activities_java = self._gateway.jvm.java.util.ArrayList()
        groups_java = self._gateway.jvm.java.util.ArrayList()
        times_java = self._gateway.jvm.java.util.ArrayList()

        for i in range(prefix, len(activities)):
            activities_java.append(str(get_int_from_unicode(activities[i])))
            groups_java.append(str(get_int_from_unicode(groups[i])))
            times_java.append(times[i])
        if not activities_java:
            return False

        return self._traces_checker.isTraceWithDataViolated(model_file, trace_id, activities_java, groups_java,
                                                            times_java)

    def verify_with_elapsed_time(self, model_file, trace_id, activities, groups, elapsed_times, times, prefix=0):

        activities_java = self._gateway.jvm.java.util.ArrayList()
        groups_java = self._gateway.jvm.java.util.ArrayList()
        elapsed_times_java = self._gateway.jvm.java.util.ArrayList()
        times_java = self._gateway.jvm.java.util.ArrayList()

        for i in range(prefix, len(activities)):
            activities_java.append(str(get_int_from_unicode(activities[i])))
            groups_java.append(str(get_int_from_unicode(groups[i])))
            elapsed_times_java.append(str(get_int_from_unicode(elapsed_times[i])))
            times_java.append(times[i])
        if not activities_java:
            return False

        return self._traces_checker.isTraceWithElapsedTimeViolated(model_file, trace_id, activities_java,
                                                                   groups_java, elapsed_times_java, times_java)

    def test_analysis(self):
        self._traces_checker.testAnalysis()

    def verify_formula_as_compliant(self, trace, formula, prefix=0):
        trace_new = self._gateway.jvm.java.util.ArrayList()
        for i in range(prefix, len(trace)):
            trace_new.append(str(get_int_from_unicode(trace[i])))
        if not trace_new:
            return False
        ver = self._traces_checker.isTraceViolated(formula, trace_new) is False
        return ver

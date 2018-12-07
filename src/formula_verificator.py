"""
the purpose of this script is to build gateway with
java src that checks the Declare formula compliance with given trace

"""

from py4j.java_collections import ListConverter
from py4j.java_gateway import JavaGateway

from shared_variables import get_int_from_unicode

gateway = JavaGateway()
verificator_app = gateway.entry_point


def verify_with_data(model_file, trace_id, activities, groups, times, prefix=0):
    activities_java = gateway.jvm.java.util.ArrayList()
    groups_java = gateway.jvm.java.util.ArrayList()
    times_java = gateway.jvm.java.util.ArrayList()

    for i in range(prefix, len(activities)):
        activities_java.append(str(get_int_from_unicode(activities[i])))
        groups_java.append(str(get_int_from_unicode(groups[i])))
        times_java.append(times[i])
    if not activities_java:
        return False

    return verificator_app.isTraceWithDataViolated(model_file, trace_id, activities_java, groups_java, times_java)


def verify_with_elapsed_time(model_file, trace_id, activities, groups, elapsed_times, times, prefix=0):

    activities_java = gateway.jvm.java.util.ArrayList()
    groups_java = gateway.jvm.java.util.ArrayList()
    elapsed_times_java = gateway.jvm.java.util.ArrayList()
    times_java = gateway.jvm.java.util.ArrayList()

    for i in range(prefix, len(activities)):
        activities_java.append(str(get_int_from_unicode(activities[i])))
        groups_java.append(str(get_int_from_unicode(groups[i])))
        elapsed_times_java.append(str(get_int_from_unicode(elapsed_times[i])))
        times_java.append(times[i])
    if not activities_java:
        return False

    return verificator_app.isTraceWithElapsedTimeViolated(model_file, trace_id, activities_java, groups_java, elapsed_times_java, times_java)


# # noinspection PyProtectedMember
# def generate_xlog(traces_id, activities, groups, times):
#     # Convert lists to Java compatible format
#     traces_id_java = ListConverter().convert(traces_id, gateway._gateway_client)
#
#     activities_java = []
#     for activity in activities:
#         activities_java.append(ListConverter().convert(activity, gateway._gateway_client))
#     activities_java = ListConverter().convert(activities_java, gateway._gateway_client)
#
#     groups_java = []
#     for group in groups:
#         groups_java.append(ListConverter().convert(group, gateway._gateway_client))
#     groups_java = ListConverter().convert(groups_java, gateway._gateway_client)
#
#     times_java = []
#     for time in times:
#         times_java.append(ListConverter().convert(time, gateway._gateway_client))
#     times_java = ListConverter().convert(times_java, gateway._gateway_client)
#
#     verificator_app.generateXLog(traces_id_java, activities_java, groups_java, times_java)


def test_analysis():
    verificator_app.testAnalysis()


def verify_formula_as_compliant(trace, formula, prefix=0):
    trace_new = gateway.jvm.java.util.ArrayList()
    for i in range(prefix, len(trace)):
        trace_new.append(str(get_int_from_unicode(trace[i])))
    if not trace_new:
        return False
    ver = verificator_app.isTraceViolated(formula, trace_new) is False
    return ver

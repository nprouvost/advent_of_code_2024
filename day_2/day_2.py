# whatever imports you need

# create example code:
example = [
    "7 6 4 2 1",
    "1 2 7 8 9",
    "9 7 6 2 1",
    "1 3 2 4 5",
    "8 6 4 4 1",
    "1 3 6 7 9",
]

example2 = [
    "7 6 4 2 1",
    "1 2 7 8 9",
    "9 7 6 2 1",
    "1 3 2 4 5",
    "8 6 4 4 1",
    "1 3 6 7 9",
    "9 8 7 6 7",
    "9 8 7 6 1",
    "1 2 3 2 4",
]


# read file to list of lines
def read_file_to_list(file_path):
    with open(file_path, 'r') as file:
        lines = [line.strip() for line in file]
    return lines


def main():
    # file_path = 'day_2.txt'
    # lines_array = read_file_to_list(file_path)
    lines_array = example2

    # part 1
    reports = []
    for line in lines_array:
        list_levels = line.split()
        levels = [int(level) for level in list_levels]
        reports.append(levels)
    # well also possible with lists, but awkward arrays are more fun
    reports = ak.Array(reports)
    sorted_reports = ak.sort(reports, axis=1)
    sorted_reports_decreasing = sorted_reports[:, ::-1]
    check1 = (
        ak.all(sorted_reports_decreasing == reports, axis=1) |
        ak.all(sorted_reports == reports, axis=1)
    )
    print("check1", check1)

    differences = ak.Array([
        [abs(reports[i][j] - reports[i][j + 1]) for j in range(len(reports[i]) - 1)]
        for i in range(len(reports))
    ])
    check2 = ak.any(differences == 0, axis=1) | ak.any(differences > 3, axis=1)
    print("check2", ~check2)
    number_of_valid_reports = ak.sum(check1 & ~check2)
    print("number_of_valid_reports", number_of_valid_reports)

    # part 2

    # # more efficient
    # import numpy as np

    # filtered_reports = []
    # for i, report in enumerate(reports):
    #     if not check1[i]:
    #         # find the first index where the report is not equal to the sorted report
    #         # first, check how much the report differs to the sorted reports
    #         test_decreasing = np.where(sorted_reports_decreasing[i] != report)
    #         test_increasing = np.where(sorted_reports[i] != report)

    #         # if the report is generally decreasing, the number of times the difference to the
    #         # neighboring element is smaller than 0 should be smaller than the number of times the
    #         # difference is larger than 0

    #         difference_no_abs = np.array([report[j] - report[j + 1] for j in range(len(report) - 1)])
    #         test_general_decreasing = ak.sum(difference_no_abs > 0)
    #         test_general_increasing = ak.sum(difference_no_abs < 0)

    #         if test_general_decreasing > test_general_increasing:
    #             # two possibilities: the first index where report and sorted are not equal is problematic
    #             # or this index corresponds to another number brought there by the sorting

    #             # do the check for the second possibility: if the number in the report is smaller than the
    #             # number in the sorted report, than the number in the sorted report is the problematic one
    #             if report[test_decreasing[0][0]] < sorted_reports_decreasing[i][test_decreasing[0][0]]:
    #                 false_index = ak.argmax(report == sorted_reports_decreasing[i][test_decreasing[0][0]])
    #                 print("possibility 2 " + "decreasing failed", i, "filtered index", false_index, "other case would be", test_decreasing[0][0])  # noqa
    #                 # handle the case where the number is present twice
    #                 if ak.sum(report == sorted_reports_decreasing[i][test_decreasing[0][0]]) > 1:
    #                     report_without_one_double = ak.concatenate([report[:false_index], report[false_index + 1:]])
    #                     false_index = ak.argmax(report_without_one_double == sorted_reports_decreasing[i][test_decreasing[0][0]]) + 1  # noqa
    #             else:
    #                 # else, first possibility
    #                 false_index = test_decreasing[0][0]
    #             print("decreasing failed", i, "filtered index", false_index)
    #         else:
    #             if len(test_increasing) > 0:
    #                 if report[test_increasing[0][0]] > sorted_reports[i][test_increasing[0][0]]:
    #                     false_index = ak.argmax(report == sorted_reports[i][test_increasing[0][0]])
    #                     # handle the case where the number is present twice
    #                     if ak.sum(report == sorted_reports[i][test_increasing[0][0]]) > 1:
    #                         report_without_one_double = ak.concatenate([report[:false_index], report[false_index + 1:]])  # noqa
    #                         false_index = ak.argmax(report_without_one_double == sorted_reports[i][test_increasing[0][0]]) + 1  # noqa
    #                 else:
    #                     false_index = test_increasing[0][0]
    #                 print("increasing failed", i, "filtered index", false_index)
    #         filtered_row = ak.concatenate([report[:false_index], report[false_index + 1:]])
    #         filtered_reports.append(filtered_row)

    #     elif check2[i]:
    #         if ak.any(differences[i] == 0):
    #             filtered_row = ak.concatenate([
    #                 report[:ak.argmax(differences[i] == 0) + 1],
    #                 report[ak.argmax(differences[i] == 0) + 2:],
    #             ])
    #             filtered_reports.append(filtered_row)
    #             print("difference 0", i, "filtered index", ak.argmax(differences[i] == 0) + 1)
    #         else:
    #             if ak.any(differences[i] > 3):
    #                 filtered_row = ak.concatenate([
    #                     report[:ak.argmax(differences[i] > 3) + 1],
    #                     report[ak.argmax(differences[i] > 3) + 2:],
    #                 ])
    #                 filtered_reports.append(filtered_row)
    #                 print("difference > 3", i, "filtered index", ak.argmax(differences[i] > 3) + 1)
    #     else:
    #         filtered_reports.append(report)
    # filtered_reports = ak.Array(filtered_reports)
    # filtered_sorted_reports = ak.sort(filtered_reports, axis=1)
    # filtered_sorted_reports_decreasing = filtered_sorted_reports[:, ::-1]
    # new_check1 = (
    #     ak.all(filtered_sorted_reports_decreasing == filtered_reports, axis=1) |
    #     ak.all(filtered_sorted_reports == filtered_reports, axis=1)
    # )
    # print("new_check1", new_check1)

    # filtered_differences = ak.Array([
    #     [abs(filtered_reports[i][j] - filtered_reports[i][j + 1]) for j in range(len(filtered_reports[i]) - 1)]
    #     for i in range(len(filtered_reports))
    # ])
    # new_check2 = ak.any(filtered_differences == 0, axis=1) | ak.any(filtered_differences > 3, axis=1)
    # print("new_check2", ~new_check2)
    # number_of_valid_filtered_reports = ak.sum(new_check1 & ~new_check2)
    # print("number_of_valid_filtered_reports", number_of_valid_filtered_reports)

    # for i, report in enumerate(filtered_reports):
    #     print("valid_filtered_reports", (new_check1 & ~new_check2)[i], i, "check 1", new_check1[i], "check 2", ~new_check2[i])  # noqa

    # brute force
    number_of_valid_reports = 0
    for i, report in enumerate(reports):
        if check1[i] and ~check2[i]:
            number_of_valid_reports += 1
            continue
        for j, level in enumerate(report):
            filtered_report = ak.concatenate([report[:j], report[j + 1:]])
            sorted_filtered_report = ak.sort(filtered_report)
            sorted_filtered_report_decreasing = sorted_filtered_report[::-1]
            if ak.all(sorted_filtered_report_decreasing == filtered_report) or ak.all(sorted_filtered_report == filtered_report):  # noqa
                differences = ak.Array([abs(filtered_report[j] - filtered_report[j + 1]) for j in range(len(filtered_report) - 1)])  # noqa
                if ak.any(differences == 0) or ak.any(differences > 3):
                    continue
                else:
                    number_of_valid_reports += 1
                    break
            else:
                continue
    print("number_of_valid_reports with one element wrong or less", number_of_valid_reports)


if __name__ == "__main__":
    main()

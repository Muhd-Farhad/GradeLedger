import pandas as pd
from pathlib import Path

data_PATH = Path(__file__).parent / "data.csv"
df = pd.read_csv(data_PATH)


def retrieveData():
    return df


def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def isinteger(value):
    try:
        int(value)
        return True
    except ValueError:
        return False


def get_subjects():
    global df
    subject_list = []

    for ind in range(len(df)):
        if df.iloc[ind, 0] not in subject_list:
            subject_list.append(df.iloc[ind, 0])

    return subject_list


def get_coursework(subject):
    list = []
    for ind in range(len(df)):
        if df.iloc[ind, 0] == subject:
            if df.iloc[ind, 1] != "null":
                list.append(
                    (
                        ind,
                        df.iloc[ind, 0],
                        df.iloc[ind, 1],
                        df.iloc[ind, 2],
                        df.iloc[ind, 3],
                    )
                )
    return list


def get_all_coursework():
    list = []
    for ind in range(len(df)):
        if df.iloc[ind, 1] != "null":
            list.append(
                (
                    ind,
                    df.iloc[ind, 0],
                    df.iloc[ind, 1],
                    df.iloc[ind, 2],
                    df.iloc[ind, 3],
                )
            )
    return list


def remove_row(index=None, subject=None, coursework=None):
    global df
    df.reset_index(drop=True, inplace=True)
    if index is not None:
        df = df.drop(index)
    else:
        for ind in range(len(df)):
            if df.iloc[ind, 0] == subject:
                if df.iloc[ind, 1] == coursework:
                    df = df.drop(ind)


def add_subject(subject):
    global df
    appended = False
    for ind in range(len(df) - 1, -1, -1):
        if df.iloc[ind, 0] == subject:
            df.loc[ind + 0.5] = "Test", "null", "null", "null"
            df = df.sort_index().reset_index(drop=True)
            appended = True
            break
    if not appended:
        df.loc[len(df)] = subject, "null", "null", "null"
        df = df.sort_index().reset_index(drop=True)


def add_coursework(subject, coursework, mark, percentage):
    global df
    for ind in range(len(df) - 1, -1, -1):
        if df.iloc[ind, 0] == subject:
            if df.iloc[ind, 1] == "null" or df.iloc[ind, 2] == "null":
                df.loc[ind] = subject, coursework, mark, percentage
            else:
                df.loc[ind + 0.5] = subject, coursework, mark, percentage
                df = df.sort_index().reset_index(drop=True)
            break


def edit_coursework(subject, coursework, mark, percentage):
    global df
    df.loc[
        (df["Subject"] == subject) & (df["Coursework"] == coursework), "Marks"
    ] = mark
    df.loc[
        (df["Subject"] == subject) & (df["Coursework"] == coursework), "Percentage"
    ] = percentage


def del_subject(subject):
    global df
    df = df[df.Subject != subject]
    df.reset_index(drop=True, inplace=True)


def dataLength():
    return len(df)


def writeData():
    df.to_csv("data.csv", index=False)

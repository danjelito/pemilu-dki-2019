import pandas as pd


def get_dapil_data(df: pd.DataFrame, dapil_no: int) -> (dict, pd.DataFrame):
    """Get the dapil data that is used for Sainte Lague calculation.

    Args:
        df (pd.DataFrame): dataframe containing the full election data.
        pd (_type_): number of dapil to be analyzed.

    Returns:
        dictionary: number of partai vote + calon vote by partai.
        pd.DataFrame: calon by partai, sorted by number of vote
    """
    # get full data of dapil
    data = df.loc[df["dapil_no"] == dapil_no]

    # get partai vote
    partai_vote = (
        data.loc[:, ["partai", "partai_vote", "vote"]]
        .groupby(["partai"])
        .agg(partai_vote=("partai_vote", "mean"), vote=("vote", "sum"))
        .sum(axis=1)
        .to_dict()
    )

    # get calon vote per dapil
    calon_vote = (
        data.loc[:, ["partai", "nama", "vote"]]
        .sort_values(["partai", "vote"], ascending=False)
        .assign(rank=lambda df_: df_.groupby("partai").cumcount(ascending=True) + 1)
    )

    return partai_vote, calon_vote


def return_odd_number(index: int) -> int:
    """Get odd number based on index position.

    Args:
        index (int): index of the odd number.

    Returns:
        int: odd number.
    """
    number = (index - 1) * 2 + 1
    return number


def get_element_cum_count(input_list: list) -> list:
    """Get a list of tuples containing the element and the cumulative count.

    Args:
        input_list (list): list containing input.

    Returns:
        list: list containing tuple of (element, cum_count).
    """
    output_list = []
    element_count = {}

    for item in input_list:
        if item not in element_count:
            element_count[item] = 1
        else:
            element_count[item] += 1
        output_list.append((item, element_count[item]))

    return output_list


def get_selected_partai(partai_vote: dict, num_selected: int, with_rank=True) -> list:
    """Get partai that are selected by Sainte Lague method.

    Args:
        partai_vote (dict): dictionary {partai: vote, partai: vote...}.
                            Output from get_dapil_data function.
        num_selected (int): number of calon that is selected.
        with_rank (bool, optional): if True, return cumulative count of each partai.
                                    Defaults to False.

    Returns:
        list: list of selected partai based on Sainte Lague method.
    """
    partai_vote_copy = partai_vote.copy()
    selected_partai = []

    for round in list(range(num_selected)):
        highest_voted = max(
            partai_vote_copy, key=lambda k: partai_vote_copy[k]
        )  # current highest voted partai
        for partai, vote in partai_vote_copy.items():
            if partai == highest_voted:
                times_selected = selected_partai.count(
                    partai
                )  # how many times this partai been selected
                round_of_calon = (
                    times_selected + 1
                )  # the round of this partai to be selected
                # divide the starting vote by odd number with index = times selected
                partai_vote_copy[partai] = partai_vote[partai] / return_odd_number(
                    index=(round_of_calon + 1)  # start dividing by 3, not 1
                )
                selected_partai.append(partai)
    if with_rank:
        return get_element_cum_count(selected_partai)
    return selected_partai


def verify_if_selected(df: pd.DataFrame, selected_calon: list, dapil_no: int):
    list_selected = df.loc[
        (df["dapil_no"] == dapil_no) & (df["terpilih"] == 1), "nama"
    ].values
    for partai, calon in selected_calon:
        if calon not in list_selected:
            raise Exception(f"Calon {calon} not terpilih")


def get_selected_calon(
    calon_vote: pd.DataFrame, selected_partai: list, with_partai=True
) -> list:
    """Get calon that are seelcted based on Sainte Lague method.

    Args:
        calon_vote (pd.DataFrame): vote for all calon in a particular dapil.
        selected_partai (list): selected partai, output from get_selected_partai function.
        with_partai (bool, optional): if True, return list of (partai, calon). Defaults to False.

    Returns:
        list: list of selected calon based on Sainte Lague method.
    """
    selected_calon = []
    for partai, rank in selected_partai:
        calon = calon_vote.loc[
            (calon_vote["partai"] == partai) & (calon_vote["rank"] == rank), "nama"
        ].values[0]
        selected_calon.append(calon)

    if with_partai:
        partai = [p for p, r in selected_partai]
        selected_calon = list(zip(partai, selected_calon))

    return selected_calon

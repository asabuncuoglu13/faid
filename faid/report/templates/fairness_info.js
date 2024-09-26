fairness_info = {
    "hardware" : {
        "info": "An ML model with the same parameters (random seeds, epochs, batch-size) on different hardware can have different performance results, especially for minority groups. This is due to (1) variations in gradient flows across groups, and (2) differences in local loss surfaces.",
        "source": "Nelaturu et al. On The Fairness Impacts of Hardware Selection in Machine Learning. 2023.",
        "link": "https://arxiv.org/abs/2312.03886"
    }
}

function get_fairness_info_by_key(key) {
    return fairness_info[key]["info"] + "\n <a class='infolink' href='" + fairness_info[key]["link"] + "'>" + fairness_info[key]["source"] + "</a>";
}


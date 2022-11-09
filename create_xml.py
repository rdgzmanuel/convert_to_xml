from dict2xml import dict2xml
import pizza_analysis_cleaning
import pandas as pd
import numpy as np


def create_dictionary(names, dfs):
    report = {}
    for i in range(len(names)):
        report[names[i]] = {}
        for j in range(len(dfs[i].columns)):
            report[names[i]][dfs[i].columns[j]] = {}
            ty = str(dfs[i].dtypes[j]) 
            report[names[i]][dfs[i].columns[j]]["type"] = ty
            report[names[i]][dfs[i].columns[j]]["n_nans"] = dfs[i][dfs[i].columns[j]].isna().sum()
            report[names[i]][dfs[i].columns[j]]["n_nulls"] = dfs[i][dfs[i].columns[j]].isnull().sum()
    return report

def write_xml(xml):
    with open("2016_report.xml", "w") as file:
        file.write(xml)

if __name__ == "__main__":
    df_order_details = pd.read_csv("order_details.csv", sep = ";", encoding="latin1")
    df_orders = pd.read_csv("orders.csv", sep=";")
    df_pizzas = pd.read_csv("pizzas.csv")
    df_pizza_types = pd.read_csv("pizza_types.csv", encoding="latin1")

    # create_informe([df_orders, df_order_details, df_pizzas, df_pizza_types])

    df_orders = df_orders.sort_values("order_id")
    df_orders = df_orders.reset_index(drop=True)
    df_orders.index = np.arange(1, len(df_orders) + 1)
    df_order_details = df_order_details.sort_values("order_details_id")
    df_order_details = df_order_details.reset_index(drop=True)
    df_order_details.index = np.arange(1, len(df_order_details) + 1)

    pizza_ingredients = pizza_analysis_cleaning.create_pizza_ingredients(df_pizza_types)
    ingredients = pizza_analysis_cleaning.create_ingredients(pizza_ingredients)

    df_prices = pizza_analysis_cleaning.obtain_prices(df_pizzas)
    df_orders = pizza_analysis_cleaning.clean_orders(df_orders)
    df_order_details = pizza_analysis_cleaning.clean_order_details(pizza_ingredients, df_order_details)
    df_weekly_pizzas = pizza_analysis_cleaning.create_weekly_pizzas(df_orders, df_order_details, df_prices, pizza_ingredients)

    optimal_ingredients = pizza_analysis_cleaning.obtain_optimal(df_weekly_pizzas, pizza_ingredients, ingredients)
    
    names = ["orders", "order_details", "pizzas", "pizza_types"]
    report = create_dictionary(names, [df_orders, df_order_details, df_pizzas, df_pizza_types])
    report["ingredients"] = optimal_ingredients
    xml = dict2xml(report, indent=" "*4)
    write_xml(xml)
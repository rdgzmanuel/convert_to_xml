from dict2xml import dict2xml
import pizza_analysis
import pandas as pd


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
    with open("report.xml", "w") as file:
        file.write(xml)

if __name__ == "__main__":
    df_orders = pd.read_csv("orders.csv")
    df_order_details = pd.read_csv("order_details.csv")
    df_pizzas = pd.read_csv("pizzas.csv")
    df_pizza_types = pd.read_csv("pizza_types.csv", encoding="latin1")
    
    # pizza_analysis.elaborar_informe([df_orders, df_order_details, df_pizzas, df_pizza_types])
    pizza_ingredients = pizza_analysis.create_pizza_ingredients(df_pizza_types)
    ingredients = pizza_analysis.create_ingredients(pizza_ingredients)

    df_prices = pizza_analysis.obtain_prices(df_pizzas)
    df_weekly_pizzas = pizza_analysis.create_weekly_pizzas(df_orders, df_order_details, df_prices, pizza_ingredients)

    optimal_ingredients = pizza_analysis.obtain_optimal(df_weekly_pizzas, pizza_ingredients, ingredients)
    
    names = ["orders", "order_details", "pizzas", "pizza_types"]
    report = create_dictionary(names, [df_orders, df_order_details, df_pizzas, df_pizza_types])
    report["ingredients"] = optimal_ingredients
    xml = dict2xml(report, indent=" "*4)
    write_xml(xml)
    
    #expand_xml(optimal_ingredients, df_orders, df_order_details, df_pizzas, df_pizza_types)
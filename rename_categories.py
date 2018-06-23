import pandas as pd

transaction_categories = [
    "Other",
    "Groceries",
    "Family",
    "Fun",
    "Becca",
    "Jeff",
    "Jeff Lunches",
    "Gas",
    "Auto",
    ]

# after rename
bills = [
    "Taxes",
    "School Fees",
    "Health Insurance",
    "Tithing",
    "Fast Offerings",
    "House Payment",
    "Internet",
    "Cell Phones",
    "Electricity",
    "Auto Insurance",
    "Life Insurance",
    ]

income = [
    "Paycheck"
    ]


# remove transactions that match these descriptions
categories_to_skip = [
    "credit card payment", 
    ]

rename_description = {
    #"Aep Online Ckf"      : "Electricity",
    }

rename_category = {
    "auto insurance"      : "Auto Insurance",
    "auto & transport"    : "Auto",
    "cash & atm"          : "Household",
    "charity"             : "Tithing",
    "clothing"            : "Household",
    "fast food"           : "Fun",
    "food & dining"       : "Fun",
    "furnishings"         : "Household",
    "gas & fuel"          : "Gas",
    "groceries"           : "Groceries",
    "hair"                : "Household",
    "hobbies"             : "Household",
    "home improvement"    : "Household",
    "music"               : "Household",
    "utilities"           : "Other",
    "internet"            : "Internet",
    "life insurance"      : "Life Insurance",
    "mobile phone"        : "Cell Phones",
    "mortgage & rent"     : "House Payment",
    "movies & dvds"       : "Fun",
    "restaurants"         : "Jeff Lunches",
    "books"               : "Jeff Lunches",  # candy from the bookstore
    "service & parts"     : "Auto",
    "shopping"            : "Household",
    ""                    : "Other",
    "business services"   : "Other",
    "fees & charges"      : "Taxes",
    "home"                : "Other",
    "pharmacy"            : "Doctor/Medicine",
    "electronics & software": "Skill Crush",
    }


def rename_categories(df):
    for row in df.index:
        #print df['category'][row] 
        if pd.isnull(df['category'][row]):
            df.set_value(row, 'category', "Other")
        if df['category'][row] in rename_category:
            df.set_value(row, 'category', rename_category[df['category'][row]])
            #print df['category'][row] 

    # now remove the categories to skip
    print "removing transactions from categories_to_skip:", categories_to_skip
    for category in categories_to_skip:
        df = df[df['category'] != category]

    return df


def reorder_bills(df):
    print "sorting bills and moving them to the top"
    trans = df[~df['category'].isin(bills)]
    df_bills = df[df['category'].isin(bills)]
    #print df_bills['category']
    #df_bills['category'] = pd.Categorical(df_bills['category'], bills)
    #cat_type = pd.api.types.CategoricalDtype()
    df_bills['category'] = df_bills['category'].astype('category', categories=bills, ordered=True)
    df_bills.sort_values(by='category', inplace=True)
    ## try to add an empty row
    #df_bills.loc[' '] = ''
    df = pd.concat([df_bills, trans])

    return df



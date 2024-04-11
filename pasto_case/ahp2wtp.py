# https://www.analyticsvidhya.com/blog/2023/05/multi-criteria-decision-making-using-ahp-in-python/
import numpy as np
import pandas as pd

def ahp_attributes(ahp_df):
    # Creating an array of sum of values in each column
    sum_array = np.array(ahp_df.sum(numeric_only=True))
    # Creating a normalized pairwise comparison matrix.
    # By dividing each column cell value with the sum of the respective column.
    cell_by_sum = ahp_df.div(sum_array,axis=1)
    # Creating Priority index by taking avg of each row
    priority_df = pd.DataFrame(cell_by_sum.mean(axis=1),
                               index=ahp_df.index,columns=['priority index'])
    priority_df = priority_df.transpose()
    return priority_df

def consistency_ratio(priority_index,ahp_df):
    random_matrix = {1:0,2:0,3:0.58,4:0.9,5:1.12,6:1.24,7:1.32,
                     8:1.14,9:1.45,10:1.49,11:1.51,12:1.48,13:1.56,
                     14:1.57,15:1.59,16:1.605,17:1.61,18:1.615,19:1.62,20:1.625}
    # Check for consistency
    consistency_df = ahp_df.multiply(np.array(priority_index.loc['priority index']),axis=1)
    consistency_df['sum_of_col'] = consistency_df.sum(axis=1)
    # To find lambda max
    lambda_max_df = consistency_df['sum_of_col'].div(np.array(priority_index.transpose()
                                                              ['priority index']),axis=0)
    lambda_max = lambda_max_df.mean()
    # To find the consistency index
    consistency_index = round((lambda_max-len(ahp_df.index))/(len(ahp_df.index)-1),3)
    print(f'The Consistency Index is: {consistency_index}')
    # To find the consistency ratio
    consistency_ratio = round(consistency_index/random_matrix[len(ahp_df.index)],3)
    print(f'The Consistency Ratio is: {consistency_ratio}')
    if consistency_ratio<0.1:
        print('The model is consistent')
    else:
        print('The model is not consistent')

def supplier_priority_index(suppl_attr_df,num_attr,attr_name):
    data_dict = {}
    # To find supplier priority indices
    # Supplier priority for attr 1
    
    data_dict[f"ahp_df_suppl_{attr_name}"] = suppl_attr_df.loc[attr_name]
    # Creating an array of sum of values in each column
    data_dict[f"sum_array_suppl_{attr_name}"] = np.array(data_dict[
        f"ahp_df_suppl_{attr_name}"].sum(numeric_only=True))
    # Normalised pairwise comparison matrix
    # Dividing each column cell value with the sum of the respective column.
    data_dict[f"norm_mat_suppl_{attr_name}"] = data_dict[
        f"ahp_df_suppl_{attr_name}"].div(data_dict[f"sum_array_suppl_{attr_name}"],axis=1)
    priority_df = pd.DataFrame(data_dict[
        f"norm_mat_suppl_{attr_name}"].mean(axis=1),
                               index=suppl_attr_df.loc[attr_name].index,columns=[attr_name])
    return priority_df

# Reading the file
ahp_df = pd.read_csv('pair_wise_comparison.csv')
ahp_df.set_index('Unnamed: 0', inplace=True)

priority_index_attr = ahp_attributes(ahp_df)
print(priority_index_attr)
consistency_ratio(priority_index_attr,ahp_df)

ahp_df_1 = pd.read_csv('alternative_attribute.csv',header=[0], index_col=[0,1]) 

suppl_AF_df = supplier_priority_index(ahp_df_1,3,'Availability Factor')
suppl_DR_df = supplier_priority_index(ahp_df_1,3,'Driving Range')
suppl_AC_df = supplier_priority_index(ahp_df_1,3,'Accumulated Cost')
suppl_I_df = supplier_priority_index(ahp_df_1,5,'Incentives')
suppl_E_df = supplier_priority_index(ahp_df_1,5,'Emissions')

suppl_df = pd.concat([suppl_AF_df,suppl_DR_df,suppl_AC_df, suppl_I_df, suppl_E_df],axis=1)
suppl_norm_df = suppl_df.multiply(np.array(priority_index_attr.loc['priority index']),axis=1)
suppl_norm_df['Sum'] = suppl_norm_df.sum(axis=1)
print(round(suppl_norm_df,2))
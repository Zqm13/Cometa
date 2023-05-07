import pandas as pd
import itertools

def cometa_process(stock, vanzari):
  
  vanzari = vanzari.fillna('')
  
  def find_combination(target, numbers):
      result = None
      
      if target == 0:
          result = [0]
      elif target in numbers:
          result = [target]
      else:
          for i in range(1, len(numbers) + 1):
              combinations = itertools.combinations(numbers, i)
              for combination in combinations:
                  if sum(combination) == target:
                      result = list(combination)
                      break
              if result is not None:
                  break
      
      if result is None or sum(result) != target:
          result = []
          
      return result
  
  def process_dataframe(df, target):
      for i, row in df.iterrows():
          orig_qty = df.loc[i, 'QTY']
          if row['QTY'] < target:
              target -= row['QTY']
              df.loc[i, 'Own'] = "X"
          else:
              df.loc[i, 'QTY'] = target
              df.loc[i, 'Partial'] = "T"
              df.loc[i, 'Own'] = "X"
              new_row = row.copy()
              new_row['QTY'] = orig_qty - target
              new_row['Partial'] = "T"
              new_row['Own'] = ""
              df.loc[i, 'QTY'] = target
              df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
              target = 0
          if target == 0:
              break
      return df
  
  original_dict = stock.set_index('Material').to_dict('index')
  original_dict_2 = {
      key: {
          'VALUES': [original_dict[key]['MIN']] if original_dict[key]['MIN'] == original_dict[key]['MAX'] else list(range(original_dict[key]['MIN'], original_dict[key]['MAX']+1))    } for key in original_dict}
  
  stock_dict = {}
  for key, value in original_dict_2.items():
      stock_dict[key] = value['VALUES']
      
  list_of_materials = vanzari['Material'].tolist()
  material_sales = {k: [] for k in stock_dict}
  unique_list = list_of_materials
  
  for i in range(len(unique_list)):
      a = 0
      x = unique_list[i]
      df_1 = vanzari[vanzari['Material']==x]
      df_1_qty = df_1['QTY'].tolist()
      b = find_combination(stock_dict[x][a], df_1_qty)
      c = len(stock_dict[x])
      if b:
          material_sales[x] = b
      elif c > 1 and stock_dict[x][a+1] < stock_dict[x][-1]:
          a += 1
          b = find_combination(stock_dict[x][a], df_1_qty)
          material_sales[x] = b
      else:
          b = find_combination(stock_dict[x][0], df_1_qty)
          material_sales[x] = b
          
  partial_list = [k for k, v in material_sales.items() if not v]
  
  partial_dict = {k: stock_dict[k] for k in partial_list if k in stock_dict}
  partial_dict = {key: value[0] for key, value in partial_dict.items()}
  partial_dict_values = list(partial_dict.values())
  
  for o in range(0,len(unique_list)):
      for uf in range(0, len(vanzari.index)):
          if vanzari['Material'][uf] == unique_list[o] and vanzari['QTY'][uf] in material_sales[unique_list[o]]:
              vanzari['Own'][uf] = "X"
              del material_sales[unique_list[o]][material_sales[unique_list[o]].index(vanzari['QTY'][uf])]
  
  
  # Create new dataframes
  for code in partial_list:
      globals()['df_'+code] = pd.DataFrame(columns=vanzari.columns)
  
  # Loop through the original dataframe and add the rows to the new dataframes
  for i, row in vanzari.iterrows():
    if row['Material'] in partial_list:
        globals()['df_'+row['Material']] = pd.concat([globals()['df_'+row['Material']], row], ignore_index=True)
        vanzari = vanzari.drop(i)
  
  # Apply process_dataframe function to each new dataframe
  for x in range(len(partial_dict_values)):
      code = partial_list[x]
      globals()['df_'+code] = process_dataframe(globals()['df_'+code], partial_dict_values[x])
      vanzari = pd.concat([vanzari, globals()['df_'+code]], ignore_index=True)
  
  pd.set_option("display.max_rows", None, "display.max_columns", None)
  
  return vanzari
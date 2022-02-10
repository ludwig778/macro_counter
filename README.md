# Macro Counter

Convenient terminal application to keep track of calories/macros with a simple prompt

## Installation

Macro counter can be installed from test PyPI using a little bit customized `pip` command:

```
pip3 install --upgrade -i https://test.pypi.org/simple/ --extra-index-url https://pypi.python.org/simple macro_counter
```

## Usage

### CLI

**Register a component**

```
>>> register tomato_100gr
Registering tomato_100gr
Type (L)iquid/(S)olid: Solid
Type units (100.0) :
How much Calories : 18
How much Protein : 0.9
How much Carb : 3.9
How much Fiber : 1.2
How much Sugar : 2.6
How much Fat : 0.2
How much Saturated fat :
How much Mono insaturated fat :
How much Poly insaturated fat : 0.1
How much Trans fat :
Created: tomato_100gr
>>> register coco_milk_100ml
Registering coco_milk_100ml
Type (L)iquid/(S)olid: Liquid
Type units (100.0) :
How much Calories : 185
How much Protein : 1.6
How much Carb : 2
How much Fiber :
How much Sugar : 2
How much Fat : 19
How much Saturated fat : 17
How much Mono insaturated fat :
How much Poly insaturated fat :
How much Trans fat :
Created: coco_milk_100ml
```

**Checking component infos**

```
>>> tomato_100gr
----------------------  --------  -----
Calories                18.0
Units                   100.0 gr
Protein                 0.9       18.0%
Carb                    3.9       78.0%
Fiber                   1.2
- Sugar                 2.6       52.0%
Fat                     0.2       4.0%
- Poly insaturated fat  0.1       2.0%
----------------------  --------  -----
>>> coco_milk_100ml
---------------  --------  -----
Calories         185.0
Units            100.0 ml
Protein          1.6       7.1%
Carb             2.0       8.8%
- Sugar          2.0       8.8%
Fat              19.0      84.1%
- Saturated fat  17.0      75.2%
---------------  --------  -----
```

**Multiplying operations**

To check the nutritional facts of 2 liters of Coco milk.

```
>>> coco_milk_100ml * 20
---------------  ---------  -----
Calories         3700.0
Units            2000.0 ml
Protein          32.0       7.1%
Carb             40.0       8.8%
- Sugar          40.0       8.8%
Fat              380.0      84.1%
- Saturated fat  340.0      75.2%
---------------  ---------  -----
```

To check the nutritional facts of 2 liters of Coco milk using normalizing-to-one operation.

```
>>> coco_milk_100ml % 2000
---------------  ---------  -----
Calories         3700.0
Units            2000.0 ml
Protein          32.0       7.1%
Carb             40.0       8.8%
- Sugar          40.0       8.8%
Fat              380.0      84.1%
- Saturated fat  340.0      75.2%
---------------  ---------  -----
```

**Adding operations**

```
>>> tomato_100gr + coco_milk_100ml
----------------------  --------  -----
Calories                203.0
Units                   200.0 gr
Protein                 2.5       9.1%
Carb                    5.9       21.4%
Fiber                   1.2
- Sugar                 4.6       16.7%
Fat                     19.2      69.6%
- Saturated fat         17.0      61.6%
- Poly insaturated fat  0.1       0.4%
----------------------  --------  -----
```

**Updating existing components**

You can remove actual fields using 'r' or 'reset' keyword.

```
>>> register tomato_100gr
Updating tomato_100gr
Type (L)iquid/(S)olid (Solid) :
Type units (100.0) :
How much Calories (18.0/Reset):
How much Protein (0.9/Reset):
How much Carb (3.9/Reset):
How much Fiber (1.2/Reset):
How much Sugar (2.6/Reset):
How much Fat (0.2/Reset):
How much Saturated fat :
How much Mono insaturated fat :
How much Poly insaturated fat (0.1/Reset):
How much Trans fat :
Nothing changed
```

**Assign a single component**

You can also update the unit field, for example cooked chicken won't be as heavy as the raw one, but will still contains the macros.

```
>>> chicken_cooked = chicken_raw
Type (L)iquid/(S)olid (Solid) :
Type units (200.0) : 160
Created: chicken_cooked
```

**Assign a recipe**

Weight the product at the end of the recipe to fine tune further macro counting, corresponding to weight gain according to cooking, evaporating water, ect...

```
>>> tiramisu = eggs * 4 + almond_flour % 66 + mascarpone % 500 + erythritol * 66 * 22 + fresh_cream % 200
Type (L)iquid/(S)olid (Solid) :
Type units (1000.0) : 900
Created: tiramisu
```

**Delete a component**

```
>>> delete tomato
Component tomato deleted
```

**Display components details**

This will display each components data with their percentages over all the other.

```
>>> detail tomato_100gr + coco_milk_100ml
Name             Units    Cal    Prot    Carb    Fiber    Sugar    Fat    Sat     Poly
---------------  -------  -----  ------  ------  -------  -------  -----  ------  ------
tomato_100gr     100.0gr  18.0   0.9     3.9     1.2      2.6      0.2            0.1
                 50.0%    8.9%   36.0%   66.1%   100.0%   56.5%    1.0%           100.0%
coco_milk_100ml  100.0ml  185.0  1.6     2.0              2.0      19.0   17.0
                 50.0%    91.1%  64.0%   33.9%            43.5%    99.0%  100.0%

Total            200.0    203.0  2.5     5.9     1.2      4.6      19.2   17.0    0.1
```

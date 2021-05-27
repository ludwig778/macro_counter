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
Type (L)iquid/(S)olid: s
How much Calories : 18
How much Units : 100
How much Protein : 0.9
How much Carb : 3.9
How much Fiber : 1.2
How much Sugar : 2.6
How much Fat : 0.2
How much Saturated fat :
How much Mono sinsaturated fat :
How much Poly insaturated fat : 0.1
How much Trans fat :
Creating tomato_100gr
>>> register coco_milk_100ml
Registering coco_milk_100ml
Type (L)iquid/(S)olid: l
How much Calories : 185
How much Units : 100
How much Protein : 1.6
How much Carb : 2
How much Fiber :
How much Sugar : 2
How much Fat : 19
How much Saturated fat : 17
How much Mono sinsaturated fat :
How much Poly insaturated fat :
How much Trans fat :
Creating coco_milk_100ml
>>>
```

**Checking component infos**

```
>>> tomato_100gr
----------------------  -----  -----
Calories                 18
Units                   100
Protein                   0.9  18.0%
Carb                      3.9  78.0%
- Fiber                   1.2
- Sugar                   2.6  52.0%
Fat                       0.2  4.0%
- Poly insaturated fat    0.1  2.0%
----------------------  -----  -----
>>> coco_milk_100ml
---------------  -----  -----
Calories         185
Units            100
Protein            1.6  7.1%
Carb               2    8.8%
- Sugar            2    8.8%
Fat               19    84.1%
- Saturated fat   17    75.2%
---------------  -----  -----
```

**Multiplying operations**

To check the nutritional facts of 2 liters of Coco milk.

```
>>> coco_milk_100ml * 20
---------------  ----  -----
Calories         3700
Units            2000
Protein            32  7.1%
Carb               40  8.8%
- Sugar            40  8.8%
Fat               380  84.1%
- Saturated fat   340  75.2%
---------------  ----  -----
```

To check the nutritional facts of 2 liters of Coco milk using normalizing-to-one operation.

```
>>> coco_milk_100ml % 2000
---------------  ----  -----
Calories         3700
Units            2000
Protein            32  7.1%
Carb               40  8.8%
- Sugar            40  8.8%
Fat               380  84.1%
- Saturated fat   340  75.2%
---------------  ----  -----
```

**Adding operations**

```
>>> tomato_100gr + coco_milk_100ml
----------------------  -----  -----
Calories                382.6
Units                   270
Protein                   3.8  7.9%
Carb                      6.7  13.8%
- Fiber                   0.8
- Sugar                   5.8  12.0%
Fat                      38.1  78.3%
- Saturated fat          34    69.8%
- Poly insaturated fat    0.1  0.1%
----------------------  -----  -----
```

**Updating existing components**

You can remove actual fields using 'r' or 'reset' keyword.

```
>>> register tomato_100gr
Updating tomato_100gr
Type (L)iquid/(S)olid (Solid) :
How much Calories (18.0/Reset):
How much Units (100.0/Reset):
How much Protein (0.9/Reset):
How much Carb (3.9/Reset):
How much Fiber (1.2/Reset):
How much Sugar (2.6/Reset):
How much Fat (0.2/Reset):
How much Saturated fat :
How much Mono sinsaturated fat :
How much Poly insaturated fat (0.1/Reset):
How much Trans fat :
Updating tomato_100gr
```

**Assign a single component**

You can also update the unit field, for example cooked chicken won't be as heavy as the raw one, but will still contains the macros.

```
>>> chicken_cooked = chicken_raw
Type units (200.0) : 160
Type (L)iquid/(S)olid (Solid) :
Creating chicken_cooked
```

**Assign a recipe**

Weight the product at the end of the recipe to fine tune further macro counting, corresponding to weight gain according to cooking, evaporating water, ect...

```
>>> tiramisu = eggs * 4 + almond_flour % 66 + mascarpone % 500 + erythritol * 66 * 22 + fresh_cream % 200
Type units (1000.0) : 900
Type (L)iquid/(S)olid (Solid) :
Creating tiramisu
```

**Delete a component**

```
>>> delete tomato
Component tomato deleted
```

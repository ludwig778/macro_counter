# Macro Counter

## Basic commands

**Install the requirements**

```
python3 -m pip install -r requirements.txt -r requirements.dev.txt
```

**Launch the prompt**

```
python3 -c "from prompts.main import MainPrompt; MainPrompt().loop()"
```

## Using Docker

**Launch the prompt**

```
docker-compose run app prompt
```

## Inside the prompt

The prompt permit to register/update ingredients, and perform simple operations to check the macro/micro nutrients consumed.

**Register an ingredient**

Pushing enter without entering any value will provide 0.0 by default.

```
(counter) => register
(counter:register) => coca
CREATING coca
Name : Coca-Cola
Type (L)iquid/(S)olid : L
How much Calories : 43
How much Units : 100
How much Protein :
How much Carb : 10.6
How much Fiber : 0
How much Sugar : 10.6
How much Fat :
How much Saturated fat :
How much Mono sinsaturated fat :
How much Poly insaturated fat :
How much Trans fat :
Registered coca
(counter:register) => bacon
CREATING bacon
Name : Bacon
Type (L)iquid/(S)olid : S
How much Calories : 502
How much Units : 100
How much Protein : 19.7
How much Carb : 1.6
How much Fiber :
How much Sugar :
How much Fat : 45.5
How much Saturated fat : 15.4
How much Mono sinsaturated fat :
How much Poly insaturated fat :
How much Trans fat :
Registered bacon
```

**Checking ingredient infos**

By default, an ingredient without any multipliers, will be shown with the given amount (units).

```
(counter) => plan
(counter:plan) => coca

--------  -----  ------
Calories   43
Units     100
Carb       10.6  100.0%
- Sugar    10.6  100.0%
--------  -----  ------
```

**Multiplying operations**

To check the nutritional facts of 2 liters of Coke.

```
(counter:plan) => coca * 2000

--------  ----  ------
Calories   860
Units     2000
Carb       212  100.0%
- Sugar    212  100.0%
--------  ----  ------
```

**Adding operations**

Checking macros/calories for 330ml of Coke and 100 grams of bacon.

Also constructing a well balanced diet..

```
(counter) => plan
(counter:plan) => coca * 330 + bacon * 100

---------------  -----  -----
Calories         643.9
Units            430
Protein           19.7  19.4%
Carb              36.6  35.9%
- Sugar           35    34.4%
Fat               45.5  44.7%
- Saturated fat   15.4  15.1%
---------------  -----  -----
```

**Autocompletion**

You can get autocompletion advices when entering Shift anytime.

```
(counter:plan) =>
                   *
                   +
                   tomato
                   coco_oil
                   coco_milk
                   butter
                   coca
```

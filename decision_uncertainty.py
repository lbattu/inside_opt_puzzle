"""
Created by Leela Krishna Battu on 10/15/2025
"""
from pathlib import Path

from pulp import LpProblem, LpVariable, getSolver, LpInteger, LpMinimize

lp_file_dir = Path(__file__).parent / "lp_files"

total_acres = 100

problem = LpProblem("crop_plan", LpMinimize)
a = LpVariable("acres_a", 0, 100)
b = LpVariable("acres_b", 0, 100)
profit = LpVariable("profit", 0)
pre_sold_units_a = LpVariable("pre_sold_units_a", 0, 800 * 100, LpInteger)
pre_sold_units_b = LpVariable("pre_sold_units_b", 0, 600 * 100, LpInteger)
pre_sold_price_a = 3.9
penalty_a = 1.5
pre_sold_price_b = 3.9
penalty_b = 1.45
fixed_cost_a = 150
fixed_cost_b = 100
problem += (profit, "objective")
problem += a + b == 100

for w in [1, 0]:
    market_price_a = 2.5 * w + 4.5 * (1 - w)
    market_price_b = 5 * w + 3 * (1 - w)

    variable_cost_a = 50 * w + 200 * (1 - w)
    variable_cost_b = 150 * w + 40 * (1 - w)
    output_a = 800 * a * w + 300 * a * (1 - w)
    output_b = 150 * b * w + 600 * b * (1 - w)
    heaviside_var_a = 1 if output_a >= pre_sold_units_a else 0
    heaviside_var_b = 1 if output_b >= pre_sold_units_b else 0

    revenue_surplus_a = (output_a - pre_sold_units_a) * market_price_a + (pre_sold_units_a * pre_sold_price_a)
    revenue_deficit_a = (output_a - pre_sold_units_a) * penalty_a + (output_a * pre_sold_price_a)
    revenue_a = heaviside_var_a * revenue_surplus_a + (1 - heaviside_var_a) * revenue_deficit_a
    cost_a = a * (fixed_cost_a + variable_cost_a)
    profit_a = revenue_a - cost_a

    revenue_surplus_b = (output_b - pre_sold_units_b) * market_price_b + (pre_sold_units_b * pre_sold_price_b)
    revenue_deficit_b = (output_b - pre_sold_units_b) * penalty_b + (output_b * pre_sold_price_b)
    revenue_b = heaviside_var_b * revenue_surplus_b + (1 - heaviside_var_b) * revenue_deficit_b
    cost_b = b * (fixed_cost_b + variable_cost_b)
    profit_b = revenue_b - cost_b
    problem += profit >= profit_a + profit_b

solver = getSolver('PULP_CBC_CMD')
solver.keepFiles = True
solver.tmpDir = lp_file_dir
problem.solve(solver=solver)

print("Status:", LpProblem.solve(problem))
print("Solver:", problem.solver)
print("Optimal value:", problem.objective.value())
for v in problem.variables():
    print(v.name, "=", v.varValue)

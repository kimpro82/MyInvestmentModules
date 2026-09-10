#!/usr/bin/env julia
# ATR Risk Parameter Simulation
#
# Simulates how ATR (volatility range) and ATR_RISK_BUDGET (risk allocation %)
# drive POSITION_VALUE and STOP_RATE, and exports 2D line plots and 3D
# surface plots visualizing the results.
#
# Assumptions (not explicitly given in the PRD, confirmed with stakeholder):
#   - REFERENCE_PRICE   : 10,000 KRW, used to convert ATR (KRW) into a raw stop rate.
#   - TOTAL_BUDGET_LIMIT: 100,000,000 KRW, the capital base for ATR_RISK_BUDGET.

using Pkg
Pkg.activate(@__DIR__)

using Plots
gr()

"Format a number with thousands separators, e.g. 10000 -> \"10,000\"."
comma_format(x) = replace(string(round(Int, x)), r"(?<=[0-9])(?=(?:[0-9]{3})+(?!\d))" => ",")

const REFERENCE_PRICE = 10_000.0      # KRW, used to convert ATR into a rate
const TOTAL_BUDGET_LIMIT = 100_000_000.0  # KRW
const MIN_STOP_RATE = 0.005           # 0.5% mandatory floor

const ATR_VALUES = 100:100:1000                 # KRW, 10 points
const RISK_BUDGET_PCTS = 0.005:0.005:0.05        # fraction, 0.5%~5.0%, 10 points

"Effective stop rate: ATR normalized to REFERENCE_PRICE, floored at MIN_STOP_RATE."
effective_stop_rate(atr::Real) = max(atr / REFERENCE_PRICE, MIN_STOP_RATE)

"Position value derived from the risk budget and the effective stop rate."
function position_value(atr::Real, risk_budget_pct::Real)
    risk_budget_krw = risk_budget_pct * TOTAL_BUDGET_LIMIT
    return risk_budget_krw / effective_stop_rate(atr)
end

"Compute the full 10x10 grid of (stop_rate, position_value) for all ATR / risk budget combinations."
function simulate()
    n_atr, n_budget = length(ATR_VALUES), length(RISK_BUDGET_PCTS)
    stop_rate = Matrix{Float64}(undef, n_budget, n_atr)
    pos_value = Matrix{Float64}(undef, n_budget, n_atr)
    for (j, budget) in enumerate(RISK_BUDGET_PCTS), (i, atr) in enumerate(ATR_VALUES)
        stop_rate[j, i] = effective_stop_rate(atr) * 100      # store as %
        pos_value[j, i] = position_value(atr, budget)
    end
    return stop_rate, pos_value
end

"Build the 2-row multi-panel line plot (POSITION_VALUE / STOP_RATE vs ATR, grouped by risk budget)."
function plot_2d(stop_rate, pos_value)
    top = plot(title="POSITION_VALUE vs ATR", xlabel="ATR (KRW)", ylabel="POSITION_VALUE (KRW)",
               legend=:outertopright, legendtitle="Risk Budget", yformatter=comma_format)
    bottom = plot(title="STOP_RATE vs ATR", xlabel="ATR (KRW)", ylabel="STOP_RATE (%)",
                  legend=:outertopright, legendtitle="Risk Budget")

    for (j, budget) in enumerate(RISK_BUDGET_PCTS)
        label = string(round(budget * 100, digits=1), "%")
        plot!(top, ATR_VALUES, pos_value[j, :], label=label, marker=:circle, linewidth=2)
        plot!(bottom, ATR_VALUES, stop_rate[j, :], label=label, marker=:circle, linewidth=2)
    end

    return plot(top, bottom, layout=(2, 1), size=(1000, 1200))
end

"Build the 3D surface plots for POSITION_VALUE and STOP_RATE over the ATR x risk-budget grid."
function plot_3d(stop_rate, pos_value)
    budget_pcts = RISK_BUDGET_PCTS .* 100

    pos_surface = surface(ATR_VALUES, budget_pcts, pos_value,
                           title="POSITION_VALUE Landscape",
                           xlabel="ATR (KRW)", ylabel="ATR_RISK_BUDGET (%)", zlabel="POSITION_VALUE (KRW)",
                           color=:viridis, zformatter=comma_format, right_margin=15Plots.mm)

    stop_surface = surface(ATR_VALUES, budget_pcts, stop_rate,
                            title="STOP_RATE Landscape",
                            xlabel="ATR (KRW)", ylabel="ATR_RISK_BUDGET (%)", zlabel="STOP_RATE (%)",
                            color=:plasma, camera=(120, 30))

    return pos_surface, stop_surface
end

function main()
    output_dir = joinpath(@__DIR__, "output")
    mkpath(output_dir)

    stop_rate, pos_value = simulate()

    fig_2d = plot_2d(stop_rate, pos_value)
    savefig(fig_2d, joinpath(output_dir, "atr_risk_2d.png"))

    pos_surface, stop_surface = plot_3d(stop_rate, pos_value)
    savefig(pos_surface, joinpath(output_dir, "atr_risk_3d_position_value.png"))
    savefig(stop_surface, joinpath(output_dir, "atr_risk_3d_stop_rate.png"))

    println("Saved figures to: ", output_dir)
end

main()

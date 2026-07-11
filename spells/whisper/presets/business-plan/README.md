# Business Plan Preset

Preset ID: `business_plan`

Use this Whisper preset when the desired artifact is a business plan, investor
plan, operating plan, financing plan, partner plan, or BP substrate. The preset
turns a venture or project into a decision document: what is being built, who it
serves, why the timing matters, how it will reach customers or users, what it
costs, what evidence exists, what remains unproven, and what next witnesses will
promote or demote the plan.

The preset is generic. It can write for a startup, internal project, nonprofit,
consulting offer, research commercialization path, or product line. It should
adapt to the chosen audience without confusing audience artifacts: a deck is a
meeting-getter, a full BP is an operating/investor-confidence document, an
operating plan is a management system, and a financing package must show cash
flow and repayment/return logic.

## Use When

- The author needs a complete business-plan scaffold or draft.
- The document must separate investor story, operating reality, evidence,
  assumptions, risks, financial model, and next milestones.
- The plan needs to support a pitch deck, investor memo, lender package,
  internal operating plan, grant/public-impact plan, or diligence data room.
- The author has source material, research, financial assumptions, customer
  evidence, or an idea that must be made decision-ready.

## Preset Files

- `preset.yaml`: Whisper transport/preset contract.
- `template.md`: Draft scaffold for the generated document.

## Invocation Shape

```text
Use whisper preset business_plan.
Venture/project: <name>
Audience mode: <investor_seed | lender_financing | operating_internal | strategic_partner | public_impact | generic>
Source material: <paths or notes>
Desired output: <full BP | investor memo | deck substrate | lender package | operating plan | BP substrate>
Evidence standard: <strict | standard | exploratory>
```

## Non-Negotiables

- Start from one concrete buyer/user problem or blocked decision.
- Separate current evidence from assumptions, forecasts, and future claims.
- Write the executive summary after the plan is internally coherent.
- Keep market, traction, compliance, financial, and defensibility claims below
  the available evidence.
- Make the financial model bottom-up: price, units, costs, capacity, cash
  timing, runway, and sensitivity.
- Include a risk and demotion gate for every load-bearing claim.
- Keep the data room or appendix as an evidence registry, not a proof-by-naming
  section.
- End with the next witness queue: what must happen in the next 30/60/90 days
  or next stage to promote, revise, or kill the plan.

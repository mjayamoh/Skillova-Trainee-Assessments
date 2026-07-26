from pathlib import Path
import numpy as np
import pandas as pd

OUTPUT = Path(__file__).with_name("customer_support_tickets_messy.csv")
rng = np.random.default_rng(20260720)
n_rows = 1000
categories = np.array(["Technical", "Product Issue", "Billing", "Account Access", "General Inquiry"])
probabilities = [0.28, 0.20, 0.20, 0.18, 0.14]
selected_categories = rng.choice(categories, n_rows, p=probabilities)
parameters = {
    "Technical": (4.0, 7.5),
    "Product Issue": (4.0, 5.5),
    "Billing": (3.5, 4.0),
    "Account Access": (3.0, 2.5),
    "General Inquiry": (3.0, 1.8),
}
resolution_times = []
for category in selected_categories:
    shape, scale = parameters[category]
    value = rng.gamma(shape, scale)
    resolution_times.append(round(float(np.clip(value, 0.5, 72.0)), 2))

df = pd.DataFrame({
    "Ticket_ID": [f"TKT-{i:04d}" for i in range(1, n_rows + 1)],
    "Category": selected_categories,
    "Resolution_Time_Hours": resolution_times,
})
missing_indices = rng.choice(df.index, size=40, replace=False)
remaining_indices = df.index.difference(missing_indices)
extreme_indices = rng.choice(remaining_indices, size=10, replace=False)
df.loc[missing_indices, "Resolution_Time_Hours"] = np.nan
df.loc[extreme_indices, "Resolution_Time_Hours"] = 999999
df.to_csv(OUTPUT, index=False)
print(f"Created {OUTPUT} with {len(df)} rows.")

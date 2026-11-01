import pandas as pd

# Simulated market prices.
# This intentionally contains up, down, and sideways behavior.
prices = [
    6200, 6202, 6199, 6201, 6204,
    6203, 6200, 6202, 6205, 6207,
    6206, 6204, 6201, 6203, 6200,
    6202, 6205, 6208, 6206, 6209,
    6211, 6208, 6205, 6207, 6210,
    6208, 6204, 6201, 6203, 6200,
    6202, 6205, 6207, 6210, 6212,
    6210, 6207, 6209, 6211, 6214,
    6212, 6209, 6206, 6208, 6210,
    6213, 6215, 6212, 6210, 6213
]

df = pd.DataFrame({"close": prices})

# How far the market moved during the previous 5 bars.
df["lookback_return"] = (
    df["close"].pct_change(periods=5) * 100
)

# How far the market moved during the NEXT 5 bars.
df["forward_return"] = (
    df["close"].shift(-5).div(df["close"]).sub(1) * 100
)

# --------------------------------------------------
# TRAINING DATA
# --------------------------------------------------

# Use the first 70% of our observations to find patterns.
split = int(len(df) * 0.70)

training = df.iloc[:split]
testing = df.iloc[split:]

print("Total observations:", len(df))
print("Training observations:", len(training))
print("Testing observations:", len(testing))

# --------------------------------------------------
# FIND SIMILAR HISTORICAL MOVES
# --------------------------------------------------

target_move = 0.05
tolerance = 0.03

matches = training[
    training["lookback_return"].between(
        target_move - tolerance,
        target_move + tolerance
    )
].copy()

matches = matches.dropna(subset=["forward_return"])

# --------------------------------------------------
# ANALYZE THE MATCHES
# --------------------------------------------------

up = (matches["forward_return"] > 0).sum()
down = (matches["forward_return"] < 0).sum()

total = up + down

print("\n--- TRAINING RESULTS ---")
print("Historical matches:", total)

if total > 0:
    probability_up = up / total * 100
    probability_down = down / total * 100
    average_return = matches["forward_return"].mean()
    median_return = matches["forward_return"].median()

    print(f"UP: {up} ({probability_up:.2f}%)")
    print(f"DOWN: {down} ({probability_down:.2f}%)")
    print(f"Average forward return: {average_return:.4f}%")
    print(f"Median forward return: {median_return:.4f}%")
else:
    print("No matching historical situations found.")
    # --------------------------------------------------
# OUT-OF-SAMPLE TEST
# --------------------------------------------------

print("\n--- OUT-OF-SAMPLE TEST ---")

# Apply the exact same pattern we discovered
# using ONLY the training data.
test_signals = testing[
    testing["lookback_return"].between(
        target_move - tolerance,
        target_move + tolerance
    )
].copy()

test_signals = test_signals.dropna(subset=["forward_return"])

if len(test_signals) > 0:

    # Our prediction is DOWN because the training
    # data showed more DOWN outcomes than UP outcomes.
    prediction = "DOWN" if probability_down > probability_up else "UP"

    print("Testing signals:", len(test_signals))
    print("Model prediction:", prediction)

    # Determine what actually happened.
    if prediction == "UP":
        correct = (test_signals["forward_return"] > 0).sum()
    else:
        correct = (test_signals["forward_return"] < 0).sum()

    wrong = len(test_signals) - correct

    accuracy = correct / len(test_signals) * 100
    average_test_return = test_signals["forward_return"].mean()

    print("Correct:", correct)
    print("Wrong:", wrong)
    print(f"Test accuracy: {accuracy:.2f}%")
    print(f"Average test return: {average_test_return:.4f}%")

else:
    print("No matching testing situations found.")
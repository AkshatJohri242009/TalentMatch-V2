from collections import defaultdict


class LearningEngine:
    def __init__(self, weight_manager, feedback_store) -> None:
        self.weight_manager = weight_manager
        self.feedback_store = feedback_store

    def update_weights(self) -> dict[str, float]:
        feedback_entries = self.feedback_store.load_feedback()
        weights = self.weight_manager.load_weights()
        if not feedback_entries:
            return weights

        signals = defaultdict(float)
        for entry in feedback_entries:
            multiplier = 1 if entry["feedback_signal"].lower() == "good" else -1
            for feature, value in entry["feature_breakdown"].items():
                if feature in weights:
                    signals[feature] += multiplier * float(value)

        adjusted = dict(weights)
        for key, value in weights.items():
            signal = signals[key]
            if signal == 0:
                continue
            if signal > 0:
                adjusted[key] = value * (1 + (0.08 * signal))
            else:
                adjusted[key] = max(0.05, value * (1 + (0.08 * signal)))
        return self.weight_manager.save_weights(adjusted)

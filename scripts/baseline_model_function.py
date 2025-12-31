def evaluate_baseline(up, val_orders_user, true_baskets, k=10):
    """
    Evaluate a simple baseline recommender:
    - Recommend each user's top-K most frequently purchased products historically.

    Parameters
    ----------
    up : DataFrame 
        Must contain ["user_id", "product_id", "up_order_count"]
        (User–product historical summary)

    val_orders_user : DataFrame
        Must contain ["order_id", "user_id"] for validation orders.

    true_baskets : Series
        true_baskets[order_id] = list of actual purchased product_ids.

    k : int
        Number of top historical products to recommend.

    Returns
    -------
    dict with baseline_precision, baseline_recall, baseline_f1, baseline_df
    """

    # -----------------------------------
    # 1. Build baseline predictions per user (top-K historically purchased)
    # -----------------------------------
    baseline_preds = (
        up.sort_values(["user_id", "up_order_count"], ascending=False)
          .groupby("user_id")
          .head(k)
          .groupby("user_id")["product_id"]
          .apply(list)
    )

    # -----------------------------------
    # 2. Filter baseline to only users who appear in validation
    # -----------------------------------
    val_user_ids = val_orders_user["user_id"].unique()
    baseline_preds_val = baseline_preds.loc[
        baseline_preds.index.isin(val_user_ids)
    ]

    # -----------------------------------
    # 3. Build true basket per user
    # -----------------------------------
    true_baskets_user = (
        val_orders_user
        .merge(true_baskets.rename("true_basket"), on="order_id")
        .set_index("user_id")["true_basket"]
    )

    # Align predictions with true baskets
    eval_df = (
        true_baskets_user
        .to_frame()
        .join(baseline_preds_val.rename("pred_basket"))
        .dropna()
    )

    # -----------------------------------
    # 4. Define precision/recall/F1 function
    # -----------------------------------
    def prf(true_list, pred_list):
        t = set(true_list)
        p = set(pred_list)
        tp = len(t & p)
        if tp == 0:
            return 0, 0, 0
        precision = tp / len(p)
        recall = tp / len(t)
        f1 = 2 * precision * recall / (precision + recall)
        return precision, recall, f1

    # -----------------------------------
    # 5. Compute metrics row-by-row
    # -----------------------------------
    eval_df["precision"] = eval_df.apply(
        lambda x: prf(x.true_basket, x.pred_basket)[0], axis=1
    )
    eval_df["recall"] = eval_df.apply(
        lambda x: prf(x.true_basket, x.pred_basket)[1], axis=1
    )
    eval_df["f1"] = eval_df.apply(
        lambda x: prf(x.true_basket, x.pred_basket)[2], axis=1
    )

    # -----------------------------------
    # 6. Compute aggregated performance
    # -----------------------------------
    baseline_precision = eval_df["precision"].mean()
    baseline_recall = eval_df["recall"].mean()
    baseline_f1 = eval_df["f1"].mean()

    return {
        "baseline_precision": baseline_precision,
        "baseline_recall": baseline_recall,
        "baseline_f1": baseline_f1,
        "baseline_df": eval_df
    }

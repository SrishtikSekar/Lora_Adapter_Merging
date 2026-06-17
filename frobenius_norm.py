def frobenius_norm(deltas):
    model_norms={}
    for layer_name,delta in deltas.items():
        model_norms[layer_name]=delta.norm(p="fro").item()
    import matplotlib.pyplot as plt

    layers=list(model_norms.keys())
    values=list(model_norms.values())

    plt.figure(figsize=(14,6))
    plt.plot(range(len(values)),values)
    plt.xticks(range(len(values)),layers,rotation=90)
    plt.ylabel("Frobenius Norm")
    plt.xlabel("Layer")
    plt.title("Layer wise LoRA Update Strength")
    plt.tight_layout()
    plt.show()
# ExploreLora.py
...
if __name__ == "__main__":
    import sys, pathlib, importlib.util
    prj = pathlib.Path(__file__).parent.resolve()
    sys.path.insert(0, str(prj))

    import configs.explora as cfg
    from core.pipeline import ContentPipeline

    pipe = ContentPipeline(config=vars(cfg))

    # ----- test için generator çağır -----
    from ai.text_generator import TextGenerator
    from ai.generators import youtube

    txtgen = TextGenerator(base_url=cfg.LM_STUDIO_URL,
                           model=cfg.LM_MODEL_NAME)

    # lora_sets’i pipeline içinden alalım
    lora_sets = pipe._scan()          # yeni mini metod
    for item in lora_sets:
        meta = f"{item['Set Name']} is an AI-rendered landscape style."
        yt = youtube.generate(txtgen, item["Set Name"], meta, cfg)
        print("YT title :", yt["title"])
        print("YT desc  :\n", yt["description"][:1000], "...\n")    
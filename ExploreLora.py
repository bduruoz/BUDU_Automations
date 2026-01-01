# ExploreLora.py
if __name__ == "__main__":
    import sys, pathlib
    prj = pathlib.Path(__file__).parent.resolve()
    sys.path.insert(0, str(prj))

    import configs.explora as cfg
    from core.pipeline import ContentPipeline
    from ai.generators.youtube import YouTubeGenerator   # yeni sınıf

    pipe = ContentPipeline(config=vars(cfg))
    lora_sets = pipe._scan()

    generator = YouTubeGenerator()          # tek satır
    for item in lora_sets:
        yt = generator.generate(item, cfg)  # 2 argüman
        print("YT title :", yt["title"])
        print("YT desc  :\n", yt["description"][:1000], "...\n")
        
        
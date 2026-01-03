# ExploreLora.py
if __name__ == "__main__":
    import sys, pathlib
    prj = pathlib.Path(__file__).parent.resolve()
    sys.path.insert(0, str(prj))

    import configs.explora as cfg
    from core.pipeline import ContentPipeline
    from ai.generators.youtube import YouTubeGenerator

    pipe = ContentPipeline(config=vars(cfg))
    from data.metadata_builder import MetaFileScanner
    
    lora_sets = MetaFileScanner(cfg.BASE_DIR).scan() 

    generator = YouTubeGenerator()
    for item in lora_sets:
        yt = generator.generate(item, cfg)
        #print("YT title :", yt["title"])
        #print("YT desc  :\n", yt["description"][:1000], "...\n")
        
    results = pipe.run()
    #print("Excel çıktısı:", results["excel_path"])

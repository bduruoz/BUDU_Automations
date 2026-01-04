# BUDU AUTIMATIONS 2026
# ExploreLora.py

if __name__ == "__main__":
    import sys, pathlib
    import configs.explora_cfg as cfg
    from core.pipeline import ContentPipeline
    from ai.generators.youtube import YouTubeGenerator
    from data.metadata_builder import MetaDataBuilder

    prj = pathlib.Path(__file__).parent.resolve()
    sys.path.insert(0, str(prj))

    pipe = ContentPipeline(config=vars(cfg))
    
    lora_sets = MetaDataBuilder(cfg.BASE_DIR).scan() 

    generator = YouTubeGenerator()

    for item in lora_sets:
        yt = generator.generate(item, cfg)
        #print("YT title :", yt["title"])
        #print("YT desc  :\n", yt["description"][:1000], "...\n")
        
    results = pipe.run()
    #print("Excel çıktısı:", results["excel_path"])



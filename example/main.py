from config import cfg

if __name__ == "__main__":
    cfg.merge_from_file("config.yaml")
    cfg.freeze()

    cfg2 = cfg.clone()
    cfg2.defrost()
    cfg2.TRAIN.SCALES = (8, 16, 32)
    cfg2.freeze()

    print("cfg:")
    print(cfg)
    print("cfg2:")
    print(cfg2)

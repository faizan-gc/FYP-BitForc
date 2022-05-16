import openai

prompt = "[Justin Original Work Boots Men's Double Comfort Work Boot][boot,leather,quality]\n "

# read config file containing api key and model id


def get_feature(prompt):
    global api_key, model_id
    try:
        if api_key is None or model_id is None:
            print("In try")
            pass
    except:
        with open("config.txt", "r") as f:
            api_key = f.readline().strip()
            model_id = f.readline().strip()
        print("In except")

    description = openai.Completion.create(
        api_key=api_key,
        # model="davinci:ft-personal-2022-05-05-09-52-32",
        # model="babbage:ft-personal-2022-05-03-19-42-40",
        model=model_id,
        prompt=prompt,
        stop = "\n",
        max_tokens = 32,
        temperature = 0.5,
        best_of = 5
        )
    text = description["choices"][0]["text"].strip()
    # remove sentence after last period from text
    text = ".".join(text.split(".")[:-1]) + "."
    return text
	

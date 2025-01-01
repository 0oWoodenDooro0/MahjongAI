from env import MahjongEnv

env = MahjongEnv(render_mode="human")
observations, infos = env.reset()

while True:
    agent = list(infos.keys())[0]
    mask = None
    if agent == "discard":
        mask = infos[agent]["mask"]
    action = {agent: {"action": env.action_space(agent).sample(mask), "player": infos[agent]["player"],
                      "tile": infos[agent]["tile"], "type": infos[agent].get("type", None)}}
    observations, rewards, terminations, trucations, infos = env.step(action)
    if terminations:
        break
env.close()

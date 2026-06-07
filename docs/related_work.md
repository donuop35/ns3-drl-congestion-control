# Related Work

## Deep Reinforcement Learning for Congestion Control

### Aurora (Jay et al., 2019)
- Uses DRL (PPO) to learn congestion control policies
- Operates at packet-level with continuous action space
- Demonstrates that RL can match or exceed traditional TCP in some settings
- **Reference**: Jay, N., Rotman, N., Godfrey, B., Schapira, M., & Tamar, A. (2019). A deep reinforcement learning perspective on internet congestion control. ICML 2019.

### Pensieve (Mao et al., 2017)
- Uses A3C for adaptive video streaming rate control
- Related: treats network adaptation as RL problem
- **Reference**: Mao, H., Schwarzkopf, M., Venkatakrishnan, S. B., Meng, Z., & Alizadeh, M. (2017). Real-world performance of adaptive bitrate algorithms. IMC 2017.

### Indigo (Yan et al., 2018)
- Imitation learning + DRL for congestion control
- Uses Pantheon testbed for evaluation
- **Reference**: Yan, F. Y., Ayers, J., Wen, Z., Agrawala, M., Hong, C. Y., ... & Winstein, K. (2018). Learning in situ: a randomized experiment in video streaming. NSDI 2018.

## ns-3 and ns3-gym for DRL Research

### ns3-gym (Gawłowicz & Vallati, 2019)
- Integrates ns-3 with OpenAI Gym interface
- Enables Python-based DRL agents to interact with ns-3 simulations
- **Reference**: Gawłowicz, P., & Vallati, M. (2019). ns3-gym: Extending OpenAI gym for networking research. CoNEXT 2019.

## Traditional TCP Congestion Control

### CUBIC (Ha et al., 2008)
- **Reference**: Ha, S., Rhee, I., & Xu, L. (2008). CUBIC: a new TCP-friendly high-speed TCP variant. ACM SIGOPS 2008.

### BBR (Cardwell et al., 2017)
- **Reference**: Cardwell, N., Cheng, Y., Gunn, C. S., Yeganeh, S. H., & Jacobson, V. (2017). BBR: congestion-based congestion control. ACM Queue 2017.

## Positioning of This Work

This project does NOT claim to outperform Aurora, Pensieve, or Pantheon benchmarks. The scope is limited to:
- Demonstrating that congestion control can be modeled as a DRL MDP
- Building a reproducible ns-3 + ns3-gym pipeline
- Showing that a basic DQN agent can complete training
- Providing honest comparison with TCP baselines (NewReno, CUBIC)

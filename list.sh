printf "${COLOR_RED} OUTPUTS:\n█████████████${COLOR_NC}\n"
tail -n 30 md_outputs/*.out
printf "${COLOR_PURPLE} LOGS:\n█████████████${COLOR_NC}\n"
cat logs/*
printf "${COLOR_CYAN} MDINFO:\n█████████████${COLOR_NC}\n"
cat mdinfo

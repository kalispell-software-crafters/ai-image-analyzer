# This is a compilation of useful 'USER-DEFINED' aliases to use

alias tmux_create='tmux new -s'        # Creates new tmux session.
alias tmux_attach='tmux a -t'          # Attaches to an existing tmux session.
alias     tmux_ls='tmux ls'            # Lists all of the existing tmux sessions.
alias   tmux_kill="tmux kill-session -t " # Kill a specific Tmux session
alias        gadd='git add'                # Adds a file / directory to repository
alias        gcom='git commit -m'          # Commits any changes. Use as: gcom "Test"
alias          gp='git push origin master' # Pushes changes to 'master'
alias         gst='git status'             # Shows the status of the GIT repository.
alias       sagent="eval $(ssh-agent -s)"  # Start SSH key agent
alias          sa='conda activate'      # Activates an Anaconda environment
alias          sd='conda deactivate'    # Deactivates an Anaconda environment
alias      jl='jupyter lab --ip 0.0.0.0 --port 8890 --no-browser --allow-root'              # Opens 'Jupyter Lab'
alias       jn='jupyter notebook --ip 0.0.0.0 --port 8890 --no-browser --allow-root'        # Opens 'Jupyter Notebook'
alias      lll="ls -lah"
# Docker-related
alias       dps="docker ps -a"
alias       dprune='docker system prune -f'
alias       dallow="direnv allow"

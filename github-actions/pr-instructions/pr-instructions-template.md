<!-- Note: Commandline instructions are added into where the placeholder string first appears --->

---

- Create a github CLI alias to quickly check out the pull request (you only need to do it once).

```
git config --global alias.pr '!sh -c "git fetch upstream pull/${1}/head:pr/${1} && git switch pr/${1}"'
```

- then check out the pr into a local branch using the following command.

```
${commandlineInstructions}
```

# Project structure

***Main solution*** - *Solution.ipynb* file. You can read it as final solution.

***Application*** is based on *app.py* and *application* folder. 
You find interactive dashboards here: https://share.streamlit.io/iakubovskii7/ether_test/app.py.
You can choose period what you want and see updated statistics and visualisation.

*Parsing.ipynb* contains stripts for data extracting from etherscan via requests and beautiful soup. 

If you want to run stripts by yourself - clone repository and install packages from *requirements.txt*.

All downloaded data is storaged in *data* folder.

I divided all data into 3 types:

- general information about ether transactions (data/transactions_ether)
- general information about token transactions (data/transactions_tokens)
- full information (which I parsed) with transfers info and more detailed token transactions data

# Short resume about strategies

I highlighted 4 main periods with different strategies:

1. Sep 2020 - Apr 2021. Value of tokens in USD was quite low comparing with all periods.
2. May 2021 - Sep 2021. Value of tokens in USD reached almost historical peak and afterwards returned to zero.
3. Oct 2021 - Jan 2022. Value of tokens in USD was about around 0-50 mln dollars that correspondence with minimal historical period amount.
4. Feb 2022 - Now. User incredibly increased his tokens in USD value.


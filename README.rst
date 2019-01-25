ShortTreys is a python poker hand evaluation library based on treys which was created by `ihendley <https://github.com/ihendley/treys>`__ 

I have added the ability to run range vs range equity as well as 6+ short deck and triton short deck.
Just pass the argument game_variant = {'FULL_DECK', 'SHORT_DECK', 'TRITON'} into the evaluator for the different games. 

I have removed everything else from the original treys to simplify this version of the package. 

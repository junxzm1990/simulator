1. Execute the following commands to pre-process the original data:

sed -i 's/AND/\&/g' ./*.cvc
sed -i 's/OR/\|/g' ./*.cvc

2. Execute the pre_processing_let.py script to change the '=' operator in 'LET' syntax into '=='. (specify each program manually)

3. Execute the pre_processing.py script to proudce predicates and paths for each program. (specify each program manually)

4. Execute the translate_cvc_to_python.py script to produce python functions for each predicate in each program. (specify each program manually)

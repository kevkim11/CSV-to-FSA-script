

import logging

# logging.info('Started recommended_ratio')
# new_list_of_list = []
# for list in list_list:
#     new_list_of_list.append(max(list))
# denominator = max(new_list_of_list)
denominator = 3
numerator = 2

logging.info('Finished recommended_ratio')
if denominator > numerator:
    logging.info('denominator = ' + str(denominator))
    logging.info('denominator = ' + str(numerator))
    logging.info('recommended_ratio = ' + str(numerator / denominator))
    a = numerator / denominator
    print "num is "
    print a
    print numerator / denominator
else:
    logging.info('recommended_ratio = 1')
    print 1
# # chart_data = [[date, chat_search, course_search, topic_search], [date, chat_search, course_search, topic_search]]

# no_searches_chat = {
#             {
#                 "date": "05-03-23",
#                 "count": "15",
#             },
#             {
#                 "date": "08-03-23",
#                 "count": "1",
#             },
#             {
#                 "date": "15-03-23",
#                 "count": "8",
#             },
            
# }
# no_searches_course =  {
#     {
#         "date": "07-03-23",
#         "count": "15",
#     },
#     {
#         "date": "02-03-23",
#         "count": "1",
#     },
#     {
#         "date": "10-03-23",
#         "count": "5",
#     },
    
# }
# no_searches_topic =  {
#     {
#         "date": "05-03-23",
#         "count": "15",
#     },
#     {
#         "date": "09-03-23",
#         "count": "51",
#     },
#     {
#         "date": "10-03-23",
#         "count": "23",
#     },
    
# }

# chart_data = []
# # inserting chats
# if len(no_searches_chat) > 0:
#     for item in no_searches_chat:
#         date = item['date']
#         chat_count = item['total']
        
#         data = [date, chat_count, 0, 0]
#         chart_data.append(data)
# print(chart_data, "\n\n")
# #inserting course
# if len(no_searches_course) > 0:
#     for item in no_searches_course:
#         date = item['date']
#         course_count = item['total']
#         for chat in chart_data:
#             if date == chat[0]:
#                 chat[2] = course_count
#             else:
#                 data = [date, 0, course_count, 0]
#                 chart_data.append(data)
# print(chart_data, "\n\n")
# #inserting topics
# if len(no_searches_topic) > 0:
#     for item in no_searches_topic:
#         date = item['date']
#         topic_count = item['total']
#         for chat in chart_data:
#             if date == chat[0]:
#                 chat[3] = topic_count    
#             else:
#                 data = [date, 0, topic_count, 0]
#                 chart_data.append(data)
    
# print(chart_data, "\n\n")

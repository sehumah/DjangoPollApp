
#  A basic poll application, consisting of 2 parts:
#      1. A public admin site that lets people view polls and vote in them.
#      2. An admin site that lets you add, change, and delete polls.


"""
- It's silly that Questions can be published on the site that have no Choices. So, the views could check for this, 
and exclude such Questions.

- The tests would create a Question without Choices and then tests that it's not published, as well as create a similar
Question with Choices, and test that it is published

- Logged-in admin users should be allowed to see unpublished Questions, but not ordinary visitors.


<QuerySet [
1 <Question: What's up?>, 
2 <Question: How're you?>, 
3 <Question: What's going on?>, 
4 <Question: Did you eat yet?>, 
5 <Question: What was that?>, 
6 <Question: Is this in the past?>
]>
"""

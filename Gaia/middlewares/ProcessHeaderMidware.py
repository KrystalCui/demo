import random

from Gaia.user_agents import agents

class ProcessHeaderMidware():
    """process request add request info"""

    def process_request(self, request, spider):
        """
        随机从列表中获得header， 并传给user_agent进行使用
        """
        agent = random.choice(agents)
        spider.logger.info(msg='now entring download midware')
        if agent:
            request.headers['User-Agent'] = agent
            # Add desired logging message here.
            spider.logger.info(u'User-Agent is : {} {}'.format(request.headers.get('User-Agent'), request))
        pass
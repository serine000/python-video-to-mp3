## How RabbitMQ works:

The producer producing the message is not directly placing the message in the RabbitMQ queue, 
it actually sends message through an exchange. 

The exchange is a middle-man that routes the message to their correct queue. It does that routing
based on some criteria.

To use the default exchange we just assign `exchange=""` this is a direct exchange with no name
that is pre-declared by the broker. Every queue created is automatically bound to it with a routing key
which will be the queue's name.

The parameter for specifying the name of the queue we are pushing the message to is called `routing_key`.

### Scaling:
If the producer is sending in more message/requests than the downstream service can handle we will need some scaling.
This means we need to make sure our queue can accommodate multiple instances of our consumer and for that we make use
of a pattern called the **Competing Consumers Pattern**. This enables multiple concurrent consumers to process messages received
on the same messaging channel.

RabbitMQ will deliver the available message in its queue to the multiple consumers in a round-robin fashion. This ensures 
messages will be delivered evenly among the consumers.
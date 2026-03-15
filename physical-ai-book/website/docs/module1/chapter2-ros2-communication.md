---
sidebar_label: '2. ROS2 Communication'
---

# Chapter 2: ROS2 Communication

## Communication Patterns

ROS2 provides several communication patterns for nodes to interact:

### 1. Topics (Publish/Subscribe)

Nodes publish messages to topics and other nodes subscribe to receive them.

```python
# Publisher example
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class PublisherNode(Node):
    def __init__(self):
        super().__init__('publisher_node')
        self.publisher_ = self.create_publisher(String, 'topic_name', 10)
        timer_period = 0.5
        self.timer = self.create_timer(timer_period, self.timer_callback)
    
    def timer_callback(self):
        msg = String()
        msg.data = 'Hello ROS2'
        self.publisher_.publish(msg)
```

```python
# Subscriber example
class SubscriberNode(Node):
    def __init__(self):
        super().__init__('subscriber_node')
        self.subscription = self.create_subscription(
            String,
            'topic_name',
            self.listener_callback,
            10)
    
    def listener_callback(self, msg):
        self.get_logger().info(f'Received: {msg.data}')
```

### 2. Services (Request/Response)

Synchronous communication where a client sends a request and waits for a response.

### 3. Actions

For long-running tasks with feedback and cancellation support.

## Quality of Service (QoS)

ROS2 provides QoS policies to control message delivery:

- **Reliability**: Reliable vs Best Effort
- **Durability**: Transient Local vs Volatile
- **Depth**: History depth for messages

## Next Steps

Next, we'll integrate Python agents with ROS2.

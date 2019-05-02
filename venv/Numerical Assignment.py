# -*- coding: utf-8 -*-
import tensorflow as tf



tf.reset_default_graph()

x = tf.placeholder(shape = [2, 2], dtype = tf.float32, name = 'X')
b = tf.constant(value = 2, dtype = tf.float32, name = 'B')
zero_initializer = tf.initializers.zeros(dtype = tf.float32)
w = tf.get_variable(initializer = zero_initializer, shape = [2, 2], name = 'W')
mul = tf.matmul(w, x, name = 'Multiplication')
ans = tf.add(mul, b, name = 'Answer')
writer = tf.summary.FileWriter('./session.graphs', tf.get_default_graph())
x_rank = tf.rank(x)
w_rank = tf.rank(w)
b_rank = tf.rank(b)
initialize = tf.initializers.global_variables()
with tf.Session() as sess:
    sess.run(initialize)
    print(sess.run(x_rank))
    print(sess.run(w_rank))
    print(sess.run(b_rank))
    print(sess.run(ans, feed_dict = {x : [[1, 1],[1, 1]]}))



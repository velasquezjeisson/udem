resource "aws_lb" "api_lb" {
  name               = "${var.project_name}-alb"
  internal           = false
  load_balancer_type = "application"
  subnets            = [aws_subnet.public.id]

  security_groups = [aws_security_group.ec2_sg.id]
}

resource "aws_lb_target_group" "api_target_group" {
  name     = "${var.project_name}-tg"
  port     = 8000
  protocol = "HTTP"
  vpc_id   = aws_vpc.main.id

  health_check {
    path                = "/docs"
    protocol            = "HTTP"
    matcher             = "200"
    interval            = 30
    timeout             = 5
    healthy_threshold   = 2
    unhealthy_threshold = 2
  }
}

resource "aws_lb_listener" "api_listener" {
  load_balancer_arn = aws_lb.api_lb.arn
  port              = 8000
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.api_target_group.arn
  }
}

resource "aws_lb_target_group_attachment" "backend_attachments" {
  count              = length(aws_instance.backend_servers)
  target_group_arn   = aws_lb_target_group.api_target_group.arn
  target_id          = aws_instance.backend_servers[count.index].id
  port               = 8000
}

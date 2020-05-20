class Deploy:

    customer_domain = None
    provisioned_directory = None

    def __init__(self, customer_domain):
        self.customer_domain = customer_domain
        self.provisioned_directory = self.invert_customer(customer_domain)

    def invert_customer(self, customer_domain):
        buffer = list(customer_domain.split("."))
        buffer.reverse()
        return "-".join(buffer)
